const custom_sheet_create = {
    "change_input": change_input,
    "submit_sheet_settings": submit_sheet_settings,
}

function change_input(number) {
    let input = document.getElementById(number + '_field_name');
    if (input.disabled) {
        input.disabled = false;
    } else {
        input.disabled = true;
    }
}
function submit_sheet_settings(set_name) {
    let form = document.querySelector('form');
    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    form.appendChild(csrf);
    let type = document.createElement('input');
    type.value = set_name;
    type.name = "request_type";
    form.appendChild(type);
    form.method = 'post';
    form.submit();
}

export default custom_sheet_create;