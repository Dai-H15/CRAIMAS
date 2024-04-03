function select_search(name){
    let s = document.getElementById("search_item_show");
    s.innerHTML ="対象:"+  name;
    s.value = name;
    s.style.display="";
    document.getElementById("search_item_value").value = name;
};
async function search_post(search_url){
    let search_item_show = document.getElementById("search_item_show");
    let search_item_value = document.getElementById("search_item_value");
    let search_str = document.getElementById("search_str");
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
        search_url = search_url.replace("sheet_from",search_item_value.value);
        search_url = search_url.replace("where",search_str.value);
        let response = await fetch(search_url);
        let html = await response.text();
        let lists = document.getElementById("post_list");
        lists.innerHTML = html;
    }
    
}