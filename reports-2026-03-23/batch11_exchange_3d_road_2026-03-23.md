# Batch 11 Analysis Report: EPS Mid-Size DLLs (Exchange, 3DEngine, Road, MapView)

**Date:** 2026-03-23  
**Analyst:** Subagent (id: c3e36bbd-2ed6-47a6-9431-81168ac25193)  
**Tool:** idalib-mcp (IDA Pro 9.0 MCP)

---

## Summary

| DLL | Port | Status | File Size | Image Size | MD5 |
|-----|------|--------|-----------|------------|-----|
| SSExchange.dll | 12051 | ✅ Listening | 1,540,096 B | 0x187000 (~1.5MB) | c3318eed |
| SS3DEngine.dll | 12052 | ✅ Listening | 525,824 B | 0x88000 (~544KB) | e3d11f3c |
| SSRoad.dll | 12053 | ✅ Listening | 401,408 B | 0x62000 (~392KB) | f17c3df3 |
| SSMapView.dll | 12054 | ✅ Listening | 503,808 B | 0x7c000 (~500KB) | 83abf02b |

---

## 1. SSExchange.dll (Port 12051)

**Module:** SSExchange.dll | Arch: 32-bit | Base: 0x10000000  
**SHA256:** da77b6ac889d59178c8fce2dbfe1380ad64d224dc83fdd6c9e7d927ee5cb56f3

### Binary Statistics
- **Call Graph Edges:** 38,565
- **Leaf Functions:** 1,680

### Import Modules
MFC42, MSVCRT, KERNEL32, USER32, GDI32, SHELL32, OLEAUT32, BCGCBPRO940

### Key Classes Identified (from strings)
- `CDblRect`, `CIntRect`, `CPoint2D`, `CPoint3D`
- `CVector2D`, `CVector3D`, `LINELOOP`
- `CSSProgress`, `CColorInfo`, `CEpsXMLNode`, `CEpsXMLSettings`
- `CGeoBase`, `CDlgBase`, `CPointObject`, `CLineObject`, `CArea`, `CMarkNote`
- `CScaleMap`, `CSSDraw`, `CFeatureList`

### String Matches by Keyword

| Keyword | Matches | Sample Findings |
|---------|---------|----------------|
| Exchange | 9 | `SetExchangeFlag`, `GetExchangeFlag`, `ExchangeCoordNote`, `SSExchange.dll` |
| Import | 2 | `ImportCEF` (2 overloads) |
| Export | 15 | `DoExport`, `Export@CVectorOut`, `ExportBylayer`, `ExportDxf`, `ExportCEF`, `ExportCor`, `ExportNote`, `ExportPermit.DXF` |
| Vector | 15 | `CVector3D`, `CVector2D`, `CVectorIn`, `CVectorOut`, vector geometry functions |
| Raster | 8 | `raster data`, `RASTERVARIABLES`, `AcDbRasterImage`, `AcDbRasterVariables` |
| Format | 15+ | `CDataFormatDisp`, `CStdDataFormatsDisp`, `GetDataFormat` |

### Domain Focus
**Data exchange/import/export module** for EPS - handles DXF, CEF, COR file formats with both vector (CVectorIn/Out) and raster (RASTERVARIABLES) support.

---

## 2. SS3DEngine.dll (Port 12052)

**Module:** SS3DEngine.dll | Arch: 32-bit | Base: 0x10000000  
**SHA256:** 12eb912bcd362424cb51542dba199d78106e866600404bfd86f5b257afa27d80

### Binary Statistics
- **Call Graph Edges:** 6,743
- **Leaf Functions:** 902

### Key Classes/Functions (from strings)
- `CSS3DEngine` - main engine class
- `SS3D` - namespace with: `MakeLookAt`, `GetLookAt`, `MakeOrtho`, `GetOrtho`, `MakeViewport`, `PointMultMatrix`, `MatrixMultMatrix`, `InvertMatrix`
- OpenGL scene functions: `glBeginSceneEXT`, `glEndSceneEXT`
- Camera: `getCamera`, `getViewport`, `setViewMatrix`, `getProjectionMatrixAsPerspective`

### String Matches by Keyword

| Keyword | Matches | Sample Findings |
|---------|---------|----------------|
| 3D | 15+ | `GL_KHR_texture_compression_astc_sliced_3d`, `GL_NV_deep_texture3D`, `glTexImage3D`, `glCompressedTexImage3D` |
| Engine | 15 | `SS3DEngine.dll`, `CSS3DEngine`, `AddLight`, `AddPrimitiveSet`, `CalcEarthwork`, `CaptureScreen`, `CreatePcdOrthoImage` |
| Render | 15+ | OpenGL rendering: `glBeginConditionalRender`, `glEndConditionalRender`, `glRenderbufferStorageMultisampleANGLE` |
| Scene | 5 | `GL_EXT_scene_marker`, `glBeginSceneEXT`, `glEndSceneEXT`, `getSceneData` |
| Mesh | 1 | `GL_SUN_mesh_array` |
| Texture | 15+ | Extensive OpenGL texture functions and extensions |
| Light | 15+ | `glFragmentLightModelfEXT`, `glFragmentLightfvEXT`, `glGetFragmentLightfvEXT` |
| Camera | 15 | `getCamera`, `getViewport`, `setViewMatrix`, `getProjectionMatrixAsPerspective`, `getViewMatrixAsLookAt` |

### Domain Focus
**3D rendering engine** using OpenGL - provides scene management, camera controls, lighting, texture support, and primitive rendering via OSG (OpenSceneGraph) integration.

---

## 3. SSRoad.dll (Port 12053)

**Module:** SSRoad.dll | Arch: 32-bit | Base: 0x10000000  
**SHA256:** 35aeca23553f6c1e8b4fd175fbdc72d8f4eb98ac2f33313235ae19ee8bb1de0b

### Binary Statistics
- **Call Graph Edges:** 6,281
- **Leaf Functions:** 968

### Key Classes/Functions (from strings)
- `CLineObject`, `LINELOOP` - line geometry
- Road-specific: `RoadCenterCode`, `SSRoad.CreateMilage`, `SSRoad.MilageAttr`, `SSRoad.HundredPole`, `SSRoad.AdjustBlock`
- Line processing: `OrderLines`, `GetLinesSumlen`, `IsPointOnLine`, `IsPLine`, `GetLineMidPoint`

### String Matches by Keyword

| Keyword | Matches | Sample Findings |
|---------|---------|----------------|
| Road | 15 | `SSRoad.dll`, `RoadCenterCode`, `SSRoad.CreateMilage`, `SSRoad.CalcHeight`, `SSRoad.ObjTypeAttr`, `SSRoad.MilageAttr` |
| Route | 0 | No direct matches |
| Line | 15 | `GetLineStyle`, `CLineObject`, `DrawLines`, `DrawLine`, `OrderLines`, `GetLinesSumlen`, `IsPointOnLine`, `LINELOOP` |
| Horizontal | 0 | No direct matches |
| Vertical | 0 | No direct matches |
| Stake | 0 | No direct matches |
| Mile | 0 | No direct matches |
| Grade | 0 | No direct matches |

### Domain Focus
**Road design module** - handles centerline processing, mileage calculations, block adjustments. Uses `RoadCenterCode` for alignment and `MilageAttr` for chainage/stake attributes.

---

## 4. SSMapView.dll (Port 12054)

**Module:** SSMapView.dll | Arch: 32-bit | Base: 0x10000000  
**SHA256:** 325d3dce65820ad72ada4bb4823ad00a00b08e7b75037acc9eaa33e81f78d07d

### Binary Statistics
- **Call Graph Edges:** 8,311
- **Leaf Functions:** 2,694 (highest among all 4 DLLs)

### Key Classes (from strings)
- `CMapCtrl`, `CMapSite`, `CMapView` - map control/view classes
- `CSSDraw`, `CSSRuntimeMap` - drawing/rendering
- `CUserLayer`, `CLayerList` - layer management
- `CSymbolParseInfo`, `CSSISymbolParse` - symbol parsing
- `CStereoView` - stereoscopic view
- Point cloud: `CEpsPointCloud`, `CPointCloudBlock`

### String Matches by Keyword

| Keyword | Matches | Sample Findings |
|---------|---------|----------------|
| Map | 15+ | `SSMapView.dll`, `CMapCtrl`, `CMapSite`, `CMapView`, `BeforeDrawMap`, `BeginDrawBuffer` |
| View | 15+ | `CMapView`, `CStereoView`, `CSSDataTabViewCtrl`, `CalDrawRect`, `CalZoomRect` |
| Display | 8 | `CloseDisplayFilter`, `GetDisplayFilter`, `SetDisplayFilter`, `MapVirtuoZoDisplay`, `MapMatrixDisplay` |
| Render | 0 | No direct matches (display/draw functions used instead) |
| Layer | 15 | `CLayerInfo`, `GetUserLayer`, `GetLayerName`, `GetMapboxLayer`, `SetColor`, `SetlayerName`, `Layer_Legend`, `LayerDrawDetails` |
| Symbol | 13 | `CSymbolParseInfo`, `CSSISymbolParse`, `SymbolProcess`, `SymbolZoomMode`, `CreatePointSymbolGraphics` |
| Style | 3 | `FillStyle`, `SetPrtFillStyle`, `GetStyleDirection` |
| Legend | 1 | `Layer_Legend` |

### Domain Focus
**Map viewing/display module** - manages map rendering, layer control, symbol parsing, and display filtering. Contains the most functions (2,694 leaf functions) indicating complex UI and rendering logic.

---

## Technical Notes

1. **IDA MCP Server Issue:** `list_funcs` tool failed with `AttributeError: 'func_t' object has no attribute 'get_name'` - this is a known issue with this version of ida-pro-mcp.

2. **String Analysis:** All 4 DLLs responded to `find_regex` queries with appropriate domain-specific strings.

3. **Architecture:** All DLLs are 32-bit Windows modules targeting base address 0x10000000.

4. **Dependencies:** All DLLs use MFC (MFC42/BCGCBPRO940) for UI and standard CRT (MSVCRT) for runtime functions.

---

## Files Generated
- `survey_SSExchange.json` - Full survey data (~278KB)
- `survey_SS3DEngine.json` - Full survey data
- `survey_SSRoad.json` - Full survey data
- `survey_SSMapView.json` - Full survey data
