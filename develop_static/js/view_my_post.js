const view_my_post = {
    "change_active": change_active
}

function change_active(url, set_id, current_status){
    let form = document.createElement('form');
    form.method = 'post';
    form.action = url;

    let csrf = document.getElementsByName('csrfmiddlewaretoken')[0];
    form.appendChild(csrf);

    let id = document.createElement("input");
    id.value = set_id;
    csrf.type = 'hidden';
    id.name = 'RegistID';
    form.appendChild(id);

    let status = document.createElement("input");
    status.value = current_status;
    status.type = "hidden";
    status.name = "current_status";
    form.appendChild(status);
    document.body.appendChild(form);
    form.submit();
};
export default view_my_post;