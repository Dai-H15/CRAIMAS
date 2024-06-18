const edit_post = {
    "t_save": t_save,
    "init":init,
}
export default edit_post

async function t_save(){
    const s = document.querySelector('form');
    const formData = new FormData(s);
    const init = {
        method: "POST",
        body: formData
    }
    const url = s.action;
    const res = await fetch(url, init);
    const data = await res.json();
    if (data.status == "OK") {
        const toast = document.getElementById('status-toast');
        toast.className = "toast bg-info";
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerHTML = "保存しました";
      toastBootstrap.show();
    }else if(data.status == "ERROR"){
        const toast = document.getElementById('status-toast');
        toast.className = "toast bg-danger";
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerHTML = `保存に失敗しました。  理由:  ${data.message}` ;
        toastBootstrap.show();
    }else{
        document.body.innerHTML = data.message;
    }
    
    };
function init(){
    window.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    form.onsubmit = ()=>{edit_post.t_save(); return false};
    ;
});
}

