const infomation = {
    "conf_infomation": conf_infomation,
}
export default infomation;
function conf_infomation(d_id, operation, action, t_csrf){
    let form = document.createElement('form');
    form.action = action;
    form.method = "post";
    let csrf = document.createElement("input");
    csrf.name = 'csrfmiddlewaretoken';
    csrf.type = 'hidden';
    csrf.value = t_csrf;
    form.appendChild(csrf);
    let id = document.createElement("input");
    id.type = 'hidden';
    id.name = "id";
    id.value = d_id;
    form.appendChild(id);
    let ope = document.createElement("input");
    ope.type = 'hidden';
    ope.name = "operation";
    ope.value = operation;
    form.appendChild(ope);
    document.body.appendChild(form);
    form.submit();
}