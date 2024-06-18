const open_url = {
    "open_url": main,
}
export default open_url;
import open_as_window from "./open_as_window";
function main(name,width,height){
    let url = document.getElementById("id_prof_url").value;
    let toastBootstrap;
    if (!(URL.canParse(url))){
        const toast = document.getElementById('status-toast');
        toast.className = "toast bg-danger";
        toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerHTML = `表示に失敗しました<br>http または https から始まるURLを入力してください` ;
        toastBootstrap.show();
    }else{
        open_as_window.open_as_window(document.getElementById("id_prof_url").value,name,width,height)
    };
};