async function p_save(){
    const s = document.querySelector('form');
    const url = "{% url 'prof_interviewer' company_id=company_id i_name=i_name %}";
    const formData = new FormData(s);
    let toastBootstrap;
    const init = {
        method: "POST",
        body: formData
    }
    const res = await fetch(url,init);
    const data = await res.json();
    if (res.ok) {
        const toast = document.getElementById('status-toast');
        if (data.status =="OK"){
        toast.className = "toast bg-info";
         toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerHTML = `保存しました 情報: ${data.reason}`;}
        else{
            toast.className = "toast bg-danger";
             toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
            document.getElementById('toast-status').innerHTML = `保存に失敗しました。  理由:  ${data.reason}  <br>エラー項目: ${data.error_list}` ;
        };
    }else{
        const toast = document.getElementById('status-toast');
        toast.className = "toast bg-danger";
         toastBootstrap = bootstrap.Toast.getOrCreateInstance(toast);
        document.getElementById('toast-status').innerHTML = `保存に失敗しました。  理由:  ${res.statusText}` ;
    };
    toastBootstrap.show();
    };