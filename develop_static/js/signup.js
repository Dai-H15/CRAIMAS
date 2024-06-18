
const signup = {
    "init": init
}
function init(){
    document.querySelector('form').addEventListener('submit', function(event) {
    var confirmation = confirm('ユーザー名・卒業年度は修正できませんがよろしいですか？');
    if (!confirmation) {
        event.preventDefault();
    }
});
}
export default signup;
