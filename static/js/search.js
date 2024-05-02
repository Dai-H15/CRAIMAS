function select_search(name){
    let s = document.getElementById("search_item_show");
    s.innerHTML ="対象:"+  name;
    s.value = name;
    s.style.display="";
    document.getElementById("search_item_value").value = name;
};
async function search_post(search_url){
        let response = await fetch(search_url);
        let html = await response.text();
        return html
    }
async function check_and_fetch(search_url){
    let search_item_show = document.getElementById("search_item_show");
    let search_item_value = document.getElementById("search_item_value");
    let search_str = document.getElementById("search_str");
    let table = document.getElementById('post_list');
    let error = "";
    if (search_item_value.value === "") {
        error += " 検索対象項目 ";
    }
    if (search_str.value === "") {
        error += " 検索文字列 ";
    };
    if(error){
        alert(`${error}は必須です`);
    }else{
        search_item_show.innerHTML = "中...";
        table.innerHTML = '<h3 class = "text-center"> 読込中・・・ </h3>';
        search_url = search_url.replace("sheet_from",search_item_value.value);
        search_url = search_url.replace("where",search_str.value);
        table.innerHTML = await search_post(search_url);
    }
}
async function init_fetch(search_url){
    let table = document.getElementById('post_list');
    table.innerHTML = '<h3 class = "text-center"> 読込中・・・ </h3>';
    table.innerHTML = await search_post(search_url);
}

