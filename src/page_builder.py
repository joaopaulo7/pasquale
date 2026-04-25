
FORM_TEMPLATE = """
    <form action="/config", method="post">
        <h3>Server Credentials</h3>
        {creds}
        <br>
        <h3>Inference  Parameters</h3>
        {inputs}
        {dropdowns}
        <br><hr><br>
        <input type="submit" value="Update">
    </form>
    """

INPUT_TEMPLATE = """
        <label for="{field_name}">{field_label}:</label>
        <input {field_type} id="{field_name}" name="{field_name}" value={field_value}>
        <br><br>
"""

SELECT_TEMPLATE = """
    <label for="{select_name}">{select_label}:</label>
    <select id="{select_name}" name="{select_name}">
        {options}
    </select>
    <br><br>
"""

OPTION_TEMPLATE = """
        <option value="{option_name}" {option_selected}>{option_label}</option>
"""


def get_inputs(fields: list[dict] = []) -> str:
    all_fields = []
    for field in fields:
        all_fields.append(
            INPUT_TEMPLATE[:].format(**field)
        )
    return "\n".join(all_fields)


def get_dropdowns(selects: list[dict] = []) -> str:
    all_selects = []
    for select in selects:
        all_options = []
        for option in select['options']:
            all_options.append(
                OPTION_TEMPLATE.format(**option)
            )
        
        select_val = SELECT_TEMPLATE.format(
            select_name = select["select_name"],
            select_label = select["select_label"],
            options = "\n".join(all_options)
        )
        all_selects.append(select_val)

    return "\n".join(all_selects)



def fields_from_config(config: dict, options: dict) -> list[dict]:
    fields = []
    for key, value in config.items():
        if key in options:
            continue
        if isinstance(value, str):
            field_type = "type=\"text\""
        elif isinstance(value, bool):
            field_type = "type=\"checkbox\""
        elif isinstance(value, float):
            field_type = "type=\"number\" min=0 max=2 step=0.01"
        else:
            field_type = "type=\"number\""

        field = {
            "field_name": key,
            "field_label": key,
            "field_value": value,
            "field_type": field_type
        }
        fields.append(field)

    return fields


def selects_from_config(config: dict, options: dict) -> list[dict]:
    fields = []
    for key, option_values in options.items():
        values = []
        for value in option_values:
            values.append({
                "option_name": value,
                "option_label": value,
                "option_selected": "selected" if config[key] == value else ""
            })
        field = {
            "select_name": key,
            "select_label": key,
            "options": values
        }
        fields.append(field)

    return fields


def get_form(creds: dict, config: dict, options: dict) -> str:
    creds_inputs = get_inputs(
        fields_from_config(creds, options))
    inputs = get_inputs(
        fields_from_config(config, options))
    dropdowns = get_dropdowns(
        selects_from_config(config, options))

    return FORM_TEMPLATE.format(
        creds = creds_inputs,
        inputs = inputs,
        dropdowns = dropdowns)