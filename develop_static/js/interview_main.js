
const interview_main = {
    "init": init,
    "view_interview": view_interview,
}
        function view_interview(d_url, InterviewID){
            let url = d_url.replace('placeholder', InterviewID);
            wind4 = window.open(`${url}`, "view_interview"+InterviewID, "width=500,height=700,toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes");
        };
function init(){
    let wind4;
    window.addEventListener('beforeunload', function(){
        if (wind4){
            wind4.close();
        }
    });
}
export default interview_main;
