# SSRETools.dll Analysis Report
**Date:** 2026-03-23  
**Binary:** `D:\EPS2026G\SSRETools.dll` (32-bit)  
**MCP Server:** port 12011

---

## 1. Binary Overview

| Property | Value |
|----------|-------|
| Module | SSRETools.dll |
| Arch | 32-bit |
| Imagebase | 0x10000000 |
| Image Size | 0x253000 (~2.4MB) |
| MD5 | 6c430c695126d60df0e7ec8fdc17dda4 |
| Total Functions | 4702 |
| Named Functions | 2523 |
| Total Strings | 4481 |
| Segments | .text, .idata, .rdata, .data |

**Main Interface:** `CSSREToolsInterface` - implements ribbon categories, drawing, command handling

---

## 2. Real Estate Data Model (SSRETools)

### 2.1 Core Classes Hierarchy

```
CHouseManager (central manager)
├── CHouseHu / CHouseHus          (户 - Household/House unit)
├── CHouseZiRZ / CHouseZiRZs      (自然幢 - Logical building)
├── CHouseLouC / CHouseLouCs      (楼幢 - Building/Cell)
├── CHouseLuoJiZ / CHouseLuoJiZs  (逻辑幢 - Logical building number)
├── CHouseMianJK / CHouseMianJKs  (面 - Face/area)
└── CZongD / CZongDs              (幢 - Building)
```

### 2.2 Entity Definitions

| Class | Chinese | Description |
|-------|---------|-------------|
| `CHouseHu` | 户 | House unit (最小不动产单元) |
| `CHouseZiRZ` | 自然幢 | Logical natural building |
| `CHouseLouC` | 楼幢 | Building/cell entity |
| `CHouseLuoJiZ` | 逻辑幢 | Logical building number |
| `CHouseMianJK` | 面 | Face/room boundary |
| `CZongD` | 幢 | Building (physical structure) |

### 2.3 Database Tables

| Table | Purpose |
|-------|---------|
| `GeoAreaTB` | Geographic Area Table (132 xrefs) |
| `EM_HuTable` | House records |
| `EM_ZongDTable` | Building records |
| `EM_ZiRZTable` | Logical building records |
| `EM_LouCTable` | LouC building table |
| `EM_MianJKTable` | Face/room boundary table |

### 2.4 Key Fields

**EM_HuTable (House) fields:**
- `EM_HuGUIDField` - House GUID
- `EM_ShiHBWField` - Room number (室号部位)
- `EM_LouCGUIDField` - LouC GUID (楼幢GUID)
- `EM_CengHField` - Floor number (层号)
- `EM_ZiRZHField` - Building number (幢号)
- `EM_ZiRZGUIDField` - ZRZ GUID
- `EM_ZongDGUIDField` - ZD GUID (幢GUID)
- `EM_ZongDDMField` - ZD code (幢代码)
- `EM_LuoJZHField` - LuoJZ number
- `EM_DanYHField` - Unit number (单元号)
- `EM_ZongCSField` - Total floors
- `EM_GXZTField` - Status
- `EM_HuXHField` - House number (户号)
- `EM_YBDCDYHField` - Pre-registration BDCDYH

**EM_ZongDTable (Building) fields:**
- `EM_ZongDGUIDField` - Building GUID
- `EM_ZongDDMField` - Building code
- `EM_YBZDDMField` - Pre-building code

---

## 3. BDCDYH (不动产权证号) Integration

SSRETools provides comprehensive **不动产权证号 (Real Estate Certificate Number)** management:

### 3.1 BDCDYH Registration Functions

| Function | Purpose |
|----------|---------|
| `OnlineGetBDCDYHH` | Get BDCDYH from online service for House |
| `OnlineGetBDCDYHLC` | Get BDCDYH for LouC |
| `OnlineGetBDCDYHZD` | Get BDCDYH for ZD (幢) |
| `OnlineGetBDCDYHZRZ` | Get BDCDYH for ZRZ |
| `RegisterBDCDYHH` | Register BDCDYH for House |
| `RegisterBDCDYHZD` | Register BDCDYH for ZD |
| `RegisterBDCDYHZRZ` | Register BDCDYH for ZRZ |
| `FillBDCDYHZRZ` | Fill BDCDYH into ZRZ record |
| `RefreshConTableBDCDYH` | Refresh contract table BDCDYH |

### 3.2 BDCDYH Database Fields

```
ID, ZDGUID, ZDDM, BDCDYH, YWH, QLLX, DJLX, DJYY, SYQMJ, 
BDCQZH, QXDM, DJJG, DBR, DJSJ, FJ, QSZT
```

---

## 4. EM Commands (Ribbon Commands)

SSRETools registers **41 commands** via `$SDL,SSRETools,...` strings:

### House Management
| Command | Description |
|---------|-------------|
| `EMCreateHu` | Create house |
| `EMCreateSelectHu` | Create from selection |
| `EMApportionEdit` | Apportion edit |
| `EMApportionAreaCal` | Area calculation |

### Floor Data
| Command | Description |
|---------|-------------|
| `EMCreateFloorData` | Create floor data |
| `EMCreateFloorData1` | Create floor data (alt) |
| `EMOpenFloorData` | Open floor data |
| `EMCopyFloorDataToOther` | Copy floor to other |
| `EMCopySameOutlineFloorData` | Copy same outline |
| `EMDeleteSameFloorData` | Delete same outline |
| `EMHideFloorData` | Hide floor data |
| `EMShowFloorData` | Show floor data |
| `EMCopySelectionObjToFloor` | Copy selection to floor |

### Building/Block Operations
| Command | Description |
|---------|-------------|
| `EMBlockInfoEdit` | Block info edit |
| `EMBlockTop` | Block top operation |
| `CreateMidWall` | Create mid wall |
| `ZDTEdit` | ZDT edit |

### Compression/Output
| Command | Description |
|---------|-------------|
| `EMCompressCGT` | Compress CGT |
| `EMCompressFCT` | Compress FCT |
| `CMCompressZDT` | Compress ZDT |

### Reports
| Command | Description |
|---------|-------------|
| `CMOutputZHT` | Output ZHT |
| `CMOutputCQShiYQZDT` | Output CQ ShiYQ ZDT |
| `CMOutputLinQZDT` | Output LinQ ZDT |
| `CMOutputShiYQZDT` | Output ShiYQ ZDT |
| `CMOutputSYQZDT` | Output SYQ ZDT |
| `CMDJDCInfoInput` | DJDC info input |

### Real Estate Settings
| Command | Description |
|---------|-------------|
| `REProjectManager` | RE project manager |
| `RESet` | RE settings |
| `EMDisplay3DHouse` | 3D house display |
| `EMCustomRoomNOCreateMode` | Custom room number mode |

### JZD (界址点) Operations
| Command | Description |
|---------|-------------|
| `CMCREATEJZD` | Create JZD |
| `CMJZDJFPH` | JZD number |
| `CMJZDDZPH` | JZD address number |
| `CreateJZDNote` | Create JZD note |

---

## 5. SSERPTools Cross-Reference

**SSERPTools.exe** (port 12002) is **completely separate** from SSRETools:

| Property | Value |
|----------|-------|
| Module | SSERPTools.exe |
| Functions | 1631 |
| Strings | 1043 |

**Key findings:**
- NO reference to SSRETools.dll
- NO reference to BDCDYH
- NO reference to cadastral terms
- Main components: `ERPManager`, `CCDBLoginDlg`, `ExcuteScript`

SSERPTools appears to be an ERP/reporting system with its own database login and script execution, but does NOT directly integrate with SSRETools.

---

## 6. Cadastral ↔ Real Estate Linkage

### 6.1 Key Link Fields

The linkage between cadastral (SSJointSurvey/BDCDYH) and real estate (SSRETools) appears via:

1. **ZDGUID** - Links ZD (幢) in real estate to cadastral parcel
2. **BDCDYH** - 28-character不动产单元代码 linking both systems
3. **GeoAreaTB** - Geographic area table with Mark field for visibility

### 6.2 Hierarchical Relationship

```
Cadastral Parcel (BDCDYH in SSJointSurvey)
    ↓ (via ZDGUID/BDCDYH)
CZongD (幢) - Building
    ↓ (via EM_ZongDGUIDField)
CHouseZiRZ (自然幢) - Logical building  
    ↓ (via EM_ZiRZGUIDField)
CHouseLouC (楼幢) - Building/cell
    ↓ (via EM_LouCGUIDField)
CHouseHu (户) - House unit
```

### 6.3 Online/Register BDCDYH Flow

The `OnlineGetBDCDYH*` functions suggest SSRETools connects to an external 不动产权登记系统 to:
1. Fetch BDCDYH for buildings (ZD/ZRZ)
2. Register BDCDYH for houses (Hu)
3. Fill BDCDYH data into the local GeoAreaTB/EM_* tables

---

## 7. Summary

**SSRETools.dll** is the Real Estate Tools module for EPS, responsible for:
1. **Household/Unit management** - CHouseHu, CHouseHus
2. **Building management** - CZongD, CHouseLouC, CHouseZiRZ
3. **Floor data management** - Create/copy/adjust floor geometry
4. **BDCDYH certificate management** - Online fetch and local registration
5. **3D visualization** - EMDisplay3DHouse

**Cadastral ↔ Real Estate Bridge:**
- No direct DLL reference found between SSJointSurvey and SSRETools
- Linkage is through **BDCDYH** (28-char 不动产单元代码) and **ZDGUID** fields
- Database tables `EM_HuTable`, `EM_ZongDTable`, `EM_ZiRZTable` store both cadastral codes and real estate attributes
- `GeoAreaTB` provides the geographic/spatial foundation linking both domains

---

*Analysis via idalib-mcp (port 12011)*
