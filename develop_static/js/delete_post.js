const delete_post = {
    "init":init,
}

function init(){
    const deleteButton = document.getElementById("delete-button");
    deleteButton.addEventListener("click", () => {
        if (confirm("注意！削除した情報は復元できません。本当に削除しますか？")) {
            document.forms[0].submit();
        } else {
            return false;
        }
    });}

export default delete_post;