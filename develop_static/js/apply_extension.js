const apply_extension = {
    "apply_extension": main
}

export default apply_extension;

function main(url, csrf_token){
    let form = document.createElement('form');
    form.action = url;
    form.method = "post";
    let csrf = document.createElement("input");
    csrf.name = 'csrfmiddlewaretoken';
    csrf.type = 'hidden';
    csrf.value = csrf_token;
    form.appendChild(csrf);
    document.body.appendChild(form);
    form.submit();
}