function open_url(id,name,width,height){
    let url = document.getElementById(id).value;
    let toastBootstrap;
    if (!(URL.canParse(url))){
        const toast = document.getElementById('status-toast');
        toast.className = "toast bg-danger";
        toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerHTML = `表示に失敗しました<br>http または https から始まるURLを入力してください` ;
        toastBootstrap.show();
    }else{
        open_as_window(document.getElementById(id).value,name,width,height);
    };
};

let wind3;
function search_zipcode(){
    let zipcode = document.getElementById('id_zipcode').value;
    let d_url = "{% url 'get_address' 'placeholder' %}"
    let url = d_url.replace('placeholder', zipcode);
    wind3 = window.open(`${url}`, "get_address", "width=400,height=400,toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes");

};
window.addEventListener('beforeunload', function(){
if (wind3){
    wind3.close();
}
window.opener.location.reload();
});

function open_interviewer(user_url){
open_as_window(user_url.replace("interviewer_name", document.getElementById("id_interviewer").value), "interviewer_view",500,600);
};

async function t_save(url){
    const s = document.querySelector('form');
    const formData = new FormData(s);
    const init = {
        method: "POST",
        body: formData
    }
    const res = await fetch(url,init);
    if (res.ok) {
        const toast = document.getElementById('status-toast');
        toast.className = "toast bg-info";
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerText = "保存しました";
      toastBootstrap.show();
    }else{
        const toast = document.getElementById('status-toast');
        toast.className = "toast bg-danger";
        const toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerText = `保存に失敗しました。  理由:  ${res.statusText}` ;
        toastBootstrap.show();
    }
    

};
async function delete_interview(url){
    if(window.confirm("本当に削除しますか？") == false){
        return;
    }else{
    let res = await fetch(url);
    if (res.ok){
        document.getElementById('form-container').innerText = await res.text();
        }
    }}