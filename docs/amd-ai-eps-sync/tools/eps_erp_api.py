"""
EPS ERP API SDK
已验证只读接口：
- Login
- GetWorkList / getunitworktodolist
- GetFlowAndUser / getflowanduser
- GetUnitInfo / getunitinfo
- GetUnitInfoBySD / getunitinfobysd

已确认命名空间（来自接口调用 VBS）：
- WorkProgressReport / erp.pro.unithelper.unitprogressreportbyzyy
- CancelAcceptWork / erp.pro.unithelper.unitcancelaccept
- DeleteCheckInfo / erp.pro.unithelper.DeleteCheckInfo
- AddCheckRecord / erp.pro.checkhelper.addcheckrecord

谨慎接口（会改动生产数据）：
- UnitAccept / unitaccept
- WorkflowSubmit / workflowsubmit
- WorkProgressReport
- CancelAcceptWork
- DeleteCheckInfo
- AddCheckRecord
- CheckRecordUpload

已知问题：
- GetUserRoles：filter_groupname 需传 SSArcSDE.GetUserRoleNameList() 的返回值，
  传空字符串会报错"应用未注册该调用的方法实例"
- CheckRecordUpload：checkdata 格式为 "timestamp;#&*;token;#&*;iid;#&*;数据JSON"（来自初始化上传.vbs）
- GetFlowAndUser：JSON 解析失败，可能返回的是非标准格式或 GBK 编码
"""
import json
import ssl
import time
import urllib.parse
import urllib.request


class EPSERP:
    def __init__(self, base=None, timeout=20, retries=5):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.base = base or 'https://getnumber.shunde.gov.cn/sg_erp_sdqtqh/sg_webapi/erpsvc'
        self.timeout = timeout
        self.retries = retries
        self.time_token = None
        self.session_token = None
        self.userid = None
        self.user = None

    def _sleep_between(self, seconds=2):
        time.sleep(seconds)

    def _common_headers(self):
        # The server often closes TLS unexpectedly; forcing connection close makes it more stable.
        # WAF requires a browser User-Agent; otherwise it returns HTTP 403.
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'close',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36',
        }

    def _get_json(self, url, retries=None):
        retries = self.retries if retries is None else retries
        last_err = None
        for attempt in range(retries):
            try:
                req = urllib.request.Request(url, headers={'Connection': 'close', 'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=self.timeout, context=self.ctx) as resp:
                    return json.loads(resp.read())
            except Exception as e:
                last_err = e
                if attempt < retries - 1:
                    self._sleep_between(2)
        raise last_err

    def _post(self, params, retries=None):
        retries = self.retries if retries is None else retries
        data = urllib.parse.urlencode(params).encode()
        last_err = None
        for attempt in range(retries):
            try:
                req = urllib.request.Request(
                    self.base + '/CommonOperate',
                    data=data,
                    headers=self._common_headers(),
                )
                with urllib.request.urlopen(req, timeout=self.timeout, context=self.ctx) as resp:
                    raw = resp.read()
                    try:
                        return json.loads(raw.decode('utf-8'))
                    except UnicodeDecodeError:
                        # Server sometimes returns GBK-encoded Chinese in error msgs
                        try:
                            return json.loads(raw.decode('gbk'))
                        except Exception:
                            return json.loads(raw.decode('utf-8', errors='replace'))
            except Exception as e:
                last_err = e
                if attempt < retries - 1:
                    self._sleep_between(2)
        raise last_err

    def _timestamp(self):
        return str(int(time.time() * 1000))

    def GetTimeToken(self):
        body = self._get_json(self.base + '/common/erp.pro.sdgtj.GeTimeToken?timestamp=' + self._timestamp())
        self.time_token = body['data']
        return self.time_token

    def Login(self, loginname, password):
        if not self.time_token:
            self.GetTimeToken()
        body = self._post({
            '_namespace': 'erp.neto.netofficehelper.userlogin',
            'access_token': self.time_token,
            'loginname': loginname,
            'password': password,
            'grant_type': 'password',
            'clientid': 'eps',
        })
        if body.get('success'):
            self.session_token = body['data'].get('code', '')
            self.user = body['data'].get('user', {})
            self.userid = self.user.get('UserId', '')
        return body

    def _require_login(self):
        if not self.session_token or not self.userid:
            raise RuntimeError('请先调用 Login')

    def GetWorkList(self, iid='', instance_name='', page_index='1', page_size='25'):
        self._require_login()
        return self._post({
            '_namespace': 'erp.neto.netofficehelper.getunitworktodolist',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'userid': self.userid,
            'iid': iid,
            'instanceName': instance_name,
            'PageIndex': str(page_index),
            'PageSize': str(page_size),
        })

    def GetFlowAndUser(self, iid, wiid):
        self._require_login()
        return self._post({
            '_namespace': 'erp.neto.workflowhelper.getflowanduser',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'userid': self.userid,
            'iid': iid,
            'wiid': wiid,
        })

    def GetUnitInfo(self, iid, fields=''):
        self._require_login()
        return self._post({
            '_namespace': 'erp.pro.unithelper.getunitinfo',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'iid': iid,
            'fields': fields,
        })

    def GetUnitInfoBySD(self, iid):
        self._require_login()
        return self._post({
            '_namespace': 'erp.pro.unithelper.getunitinfobysd',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'iid': iid,
        })

    def GetUserRoles(self, filter_groupname=''):
        """
        角色过滤串建议传 SSArcSDE.GetUserRoleNameList() 的结果。
        直接传空字符串在部分环境会返回“应用未注册该调用的方法实例”。
        """
        self._require_login()
        return self._post({
            '_namespace': 'erp.neto.netofficehelper.GetUserRoles',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'userid': self.userid,
            'filter_groupname': filter_groupname,
        })

    def WorkProgressReport(self, iid, progresspct, progressdesc):
        """谨慎：会上报业务进度。"""
        self._require_login()
        return self._post({
            '_namespace': 'erp.pro.unithelper.unitprogressreportbyzyy',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'iid': iid,
            'progresspct': str(progresspct),
            'progressdesc': progressdesc,
        })

    def CancelAcceptWork(self, iid, wiid):
        """谨慎：会执行取消接单。"""
        self._require_login()
        return self._post({
            '_namespace': 'erp.pro.unithelper.unitcancelaccept',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'iid': iid,
            'wiid': wiid,
        })

    def DeleteCheckInfo(self, iid):
        """谨慎：删除指定业务已有质检记录。"""
        self._require_login()
        return self._post({
            '_namespace': 'erp.pro.unithelper.DeleteCheckInfo',
            'access_token': self.session_token,
            'iid': iid,
        })

    def AddCheckRecord(self, iid, checkdata):
        """谨慎：新增质检记录，checkdata 应为服务端要求的 JSON 结构。"""
        self._require_login()
        return self._post({
            '_namespace': 'erp.pro.checkhelper.addcheckrecord',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'iid': iid,
            'checkdata': checkdata,
        })

    def CheckRecordUpload(self, iid, checkdata, delete_first=True):
        """
        对应脚本“质检记录上传.vbs”：先删后传。
        返回 {'delete': ..., 'add': ...} 便于排障。
        """
        result = {'delete': None, 'add': None}
        if delete_first:
            result['delete'] = self.DeleteCheckInfo(iid)
        result['add'] = self.AddCheckRecord(iid, checkdata)
        return result

    def UnitAccept(self, iid, wiid):
        """谨慎：真实接单动作，默认不要在生产数据上直接调用。"""
        self._require_login()
        return self._post({
            '_namespace': 'erp.pro.unithelper.unitaccept',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'iid': iid,
            'wiid': wiid,
        })

    def WorkflowSubmit(self, iid, wiid, users):
        """谨慎：真实提交流程动作，默认不要在生产数据上直接调用。"""
        self._require_login()
        return self._post({
            '_namespace': 'erp.neto.workflowhelper.workflowsubmit',
            '_timestamp': self._timestamp(),
            'access_token': self.session_token,
            'userid': self.userid,
            'iid': iid,
            'wiid': wiid,
            'users': users,
        })

    def FindWorkItem(self, iid, page_size='200'):
        worklist = self.GetWorkList(page_index='1', page_size=page_size)
        items = worklist.get('data', {}).get('DataTable', [])
        for item in items:
            if item.get('iid') == iid:
                return item
        return None


if __name__ == '__main__':
    api = EPSERP()
    login = api.Login('曾玮', '281436G52v364i.')
    print('login.success =', login.get('success'))
    print('userid =', api.userid)

    worklist = api.GetWorkList(page_index='1', page_size='25')
    items = worklist.get('data', {}).get('DataTable', [])
    print('worklist.count =', len(items))
    if items:
        first = items[0]
        print('first =', first.get('iid'), first.get('name'), first.get('step'))

        flow = api.GetFlowAndUser(first['iid'], first['wiid'])
        print('getflowanduser.success =', flow.get('success'))

        unit = api.GetUnitInfo(first['iid'])
        print('getunitinfo.success =', unit.get('success'))

        unit_sd = api.GetUnitInfoBySD(first['iid'])
        print('getunitinfobysd.success =', unit_sd.get('success'))
