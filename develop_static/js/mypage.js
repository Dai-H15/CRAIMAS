import search from "./search";
function init(url){
    document.addEventListener("DOMContentLoaded", async function() {
    await search.init_fetch(url);
});
}

const mypage = {
    "init": init
}
export default mypage;

