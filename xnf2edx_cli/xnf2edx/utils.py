from xnf2edx.consts import (
    CDATOSGENERALESROW,
    CDATOSGENERALESSHEET,
    CONF_SHEET,
    CDATOSGENERALESVERSIONPOS,
    CONFVERSIONPOS,
)


def get_all_row_values(sheet, row):
    content = []
    for col in range(sheet.ncols):
        aux = sheet.cell_value(row, col)
        content.append(aux)
    content = list(filter(lambda x: x.strip() != "", content))
    return content


def get_sheet_from_namespace(wb, names):
    sheet = None
    for tag in names:
        try:
            sheet = wb.sheet_by_name(tag)
            break
        except Exception:
            pass
    if sheet is None:
        raise Exception(f"No sheet found with any of the names in {names}")
    return sheet


def get_sheet_from_row(wb, row):
    tags = get_all_row_values(wb.sheet_by_name(CONF_SHEET), row)
    return get_sheet_from_namespace(wb, tags)


def get_sheet(wb, sheet_name, row):
    try:
        sheet = wb.sheet_by_name(sheet_name)
    except Exception:
        sheet = get_sheet_from_row(wb, row)
    return sheet


def get_values_with_fallback(wb, row, fb):
    try:
        conf_sheet = wb.sheet_by_name(CONF_SHEET)
        values = get_all_row_values(conf_sheet, row)
    except Exception:
        values = [fb]
    return values


def get_version(wb):
    try:
        conf_sheet = wb.sheet_by_name(CONF_SHEET)
        version = conf_sheet.cell_value(CONFVERSIONPOS[0], CONFVERSIONPOS[1])
    except Exception:
        datos_generales_sheet = get_sheet(wb, CDATOSGENERALESSHEET, CDATOSGENERALESROW)
        version = datos_generales_sheet.cell_value(
            CDATOSGENERALESVERSIONPOS[0], CDATOSGENERALESVERSIONPOS[1]
        )
    return version
