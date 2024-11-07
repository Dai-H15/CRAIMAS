var Main;(()=>{"use strict";var e,t,n={},o={};function a(e){var t=o[e];if(void 0!==t)return t.exports;var s=o[e]={exports:{}};return n[e](s,s.exports,a),s.exports}a.m=n,a.d=(e,t)=>{for(var n in t)a.o(t,n)&&!a.o(e,n)&&Object.defineProperty(e,n,{enumerable:!0,get:t[n]})},a.f={},a.e=e=>Promise.all(Object.keys(a.f).reduce(((t,n)=>(a.f[n](e,t),t)),[])),a.u=e=>e+".main.js",a.g=function(){if("object"==typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"==typeof window)return window}}(),a.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),e={},t="Main:",a.l=(n,o,s,d)=>{if(e[n])e[n].push(o);else{var c,i;if(void 0!==s)for(var l=document.getElementsByTagName("script"),r=0;r<l.length;r++){var m=l[r];if(m.getAttribute("src")==n||m.getAttribute("data-webpack")==t+s){c=m;break}}c||(i=!0,(c=document.createElement("script")).charset="utf-8",c.timeout=120,a.nc&&c.setAttribute("nonce",a.nc),c.setAttribute("data-webpack",t+s),c.src=n),e[n]=[o];var u=(t,o)=>{c.onerror=c.onload=null,clearTimeout(g);var a=e[n];if(delete e[n],c.parentNode&&c.parentNode.removeChild(c),a&&a.forEach((e=>e(o))),t)return t(o)},g=setTimeout(u.bind(null,void 0,{type:"timeout",target:c}),12e4);c.onerror=u.bind(null,c.onerror),c.onload=u.bind(null,c.onload),i&&document.head.appendChild(c)}},a.r=e=>{"undefined"!=typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},(()=>{var e;a.g.importScripts&&(e=a.g.location+"");var t=a.g.document;if(!e&&t&&(t.currentScript&&(e=t.currentScript.src),!e)){var n=t.getElementsByTagName("script");if(n.length)for(var o=n.length-1;o>-1&&(!e||!/^http(s?):/.test(e));)e=n[o--].src}if(!e)throw new Error("Automatic publicPath is not supported in this browser");e=e.replace(/#.*$/,"").replace(/\?.*$/,"").replace(/\/[^\/]+$/,"/"),a.p=e})(),(()=>{var e={792:0};a.f.j=(t,n)=>{var o=a.o(e,t)?e[t]:void 0;if(0!==o)if(o)n.push(o[2]);else{var s=new Promise(((n,a)=>o=e[t]=[n,a]));n.push(o[2]=s);var d=a.p+a.u(t),c=new Error;a.l(d,(n=>{if(a.o(e,t)&&(0!==(o=e[t])&&(e[t]=void 0),o)){var s=n&&("load"===n.type?"missing":n.type),d=n&&n.target&&n.target.src;c.message="Loading chunk "+t+" failed.\n("+s+": "+d+")",c.name="ChunkLoadError",c.type=s,c.request=d,o[1](c)}}),"chunk-"+t,t)}};var t=(t,n)=>{var o,s,[d,c,i]=n,l=0;if(d.some((t=>0!==e[t]))){for(o in c)a.o(c,o)&&(a.m[o]=c[o]);i&&i(a)}for(t&&t(n);l<d.length;l++)s=d[l],a.o(e,s)&&e[s]&&e[s][0](),e[s]=0},n=self.webpackChunkMain=self.webpackChunkMain||[];n.forEach(t.bind(null,0)),n.push=t.bind(null,n.push.bind(n))})();var s={};a.r(s),a.d(s,{default:()=>T});const d={t_save:async function(){const e=document.querySelector("form"),t={method:"POST",body:new FormData(e)},n=e.action,o=await fetch(n,t),a=await o.json();if("OK"==a.status){const e=document.getElementById("status-toast");e.className="toast bg-info";const t=bootstrap.Toast.getOrCreateInstance(e);document.getElementById("toast-status").innerHTML="保存しました",t.show()}else if("ERROR"==a.status){const e=document.getElementById("status-toast");e.className="toast bg-danger";const t=bootstrap.Toast.getOrCreateInstance(e);document.getElementById("toast-status").innerHTML=`保存に失敗しました。  理由:  ${a.message}`,t.show()}else document.body.innerHTML=a.message},init:function(){window.addEventListener("DOMContentLoaded",(()=>{document.querySelector("form").onsubmit=()=>(d.t_save(),!1)}))}},c={wind:[],init:function(){window.addEventListener("beforeunload",(function(){if(0!=c.wind.length)for(let e=0;e<c.wind.length;e++)c.wind[e].close()}))},open_as_window:function(e,t,n,o){c.wind.push(window.open(`${e}`,`${t}`,`width=${n},height=${o},toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes`))},pop:function(){c.wind.pop()}},i=c,l={init:function(){window.addEventListener("beforeunload",(function(){window.opener.location.reload()}));let e=document.getElementById("auto-save-check");e.addEventListener("click",(()=>{e.checked?function(){const e=document.getElementById("status-toast");e.className="toast bg-success";const t=bootstrap.Toast.getOrCreateInstance(e);document.getElementById("toast-status").innerHTML="自動保存が有効化されました",t.show();const n=document.getElementById("time-toast");n.className="toast bg-info";const o=bootstrap.Toast.getOrCreateInstance(n);document.getElementById("time-toast-status").innerHTML="最後に自動保存された時刻が表示されます",o.show(),l.id_autosave=setInterval((()=>{r(!0)}),3e4)}():m()}))},open_url:function(e,t,n,o){let a,s=document.getElementById(e).value;if(URL.canParse(s))i.open_as_window(document.getElementById(e).value,t,n,o);else{const e=document.getElementById("status-toast");e.className="toast bg-danger",a=bootstrap.Toast.getOrCreateInstance(e),document.getElementById("toast-status").innerHTML="表示に失敗しました<br>http または https から始まるURLを入力してください",a.show()}},delete_interview:async function(e){if(0!=window.confirm("本当に削除しますか？")){let t=await fetch(e);t.ok&&(document.getElementById("form-container").innerText=await t.text())}},search_zipcode:function(e){let t=document.getElementById("id_zipcode").value,n=e.replace("placeholder",t);wind3=window.open(`${n}`,"get_address","width=400,height=400,toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes")},open_interviewer:function(e){if(!document.getElementById("id_interviewer").value.trim()){let e;const t=document.getElementById("status-toast");return t.className="toast bg-danger",e=bootstrap.Toast.getOrCreateInstance(t),document.getElementById("toast-status").innerHTML="表示に失敗しました<br>検索・登録したい担当者名を入力してください。",void e.show()}i.open_as_window(e.replace("interviewer_name",document.getElementById("id_interviewer").value),"interviewer_view",500,600)},t_save:r,ai_loading_change:u,get_note_summary:async function(){const e=document.getElementById("config"),t=e.action,n=new FormData(e);let o=document.getElementById("status-toast"),a=bootstrap.Toast.getOrCreateInstance(o);const s=document.getElementById("id_summary");try{await Main.default.interview.t_save(!1)}catch{return}const d={method:"POST",body:n};try{u();let e=await fetch(t,d),n=await e.json();"error"===n.status&&(u(),o=document.getElementById("status-toast"),o.className="toast bg-danger",a=bootstrap.Toast.getOrCreateInstance(o),document.getElementById("toast-status").innerHTML=n.reason,a.show()),"NG"===n.status&&(o=document.getElementById("status-toast"),o.className="toast bg-danger",a=bootstrap.Toast.getOrCreateInstance(o),document.getElementById("toast-status").innerHTML=n.reason,a.show()),"ok"===n.status&&(u(),o=document.getElementById("status-toast"),o.className="toast bg-success",a=bootstrap.Toast.getOrCreateInstance(o),document.getElementById("toast-status").innerHTML=n.reason,a.show(),s.value=`\n-----\n要約\n-----\n${n.result.summary}\r\n\n\n-----\nアドバイス\n-----\n${n.result.advice}\r\n\n`)}catch{return u(),o=document.getElementById("status-toast"),o.className="toast bg-danger",a=bootstrap.Toast.getOrCreateInstance(o),document.getElementById("auto-save-check").checked=!1,void a.show()}},id_autosave:"initialized"};async function r(e){const t=document.getElementById("interview-form").action,n=document.getElementById("interview-form"),o=new FormData(n);let a,s,d=document.getElementById("status-toast"),c=bootstrap.Toast.getOrCreateInstance(d);const i={method:"POST",body:o};try{a=await fetch(t,i),s=await a.json()}catch{if("initialized"!=l.id_autosave){const e=document.getElementById("time-toast"),t=bootstrap.Toast.getOrCreateInstance(e);e.className="toast bg-danger",document.getElementById("auto-save-check").checked=!1,m(),t.show()}d.className="toast bg-danger",document.getElementById("toast-status").innerHTML="保存に失敗しました。ネットワーク接続を確認してください。",c.show()}s.is_saved?!1===e?(d=document.getElementById("status-toast"),d.className="toast bg-info",c=bootstrap.Toast.getOrCreateInstance(d),document.getElementById("toast-status").innerHTML=`保存しました  保存時刻${s.saved_time.slice(0,8)}`,c.show()):document.getElementById("time-toast-status").innerHTML=`最終保存時刻: ${s.saved_time.slice(0,8)}`:(d=document.getElementById("status-toast"),d.className="toast bg-danger",c=bootstrap.Toast.getOrCreateInstance(d),document.getElementById("auto-save-check").checked=!1,m(),document.getElementById("toast-status").innerHTML=`保存に失敗しました。 <br> 理由:  ${s.errors}`,c.show())}function m(){clearInterval(l.id_autosave);const e=document.getElementById("status-toast");e.className="toast bg-secondary";const t=bootstrap.Toast.getOrCreateInstance(e);document.getElementById("toast-status").innerHTML="自動保存が無効化されました",t.show();const n=document.getElementById("time-toast");bootstrap.Toast.getOrCreateInstance(n).hide()}function u(){let e=document.getElementById("ai-button"),t=document.getElementById("ai-status-loading-text"),n=document.getElementById("ai-status-loading-spin"),o=document.getElementById("ai-status-waiting");const a=o.hidden;t.hidden=a,n.hidden=a,e.disabled=!a,o.hidden=!a}const g={select_search:function(e){let t=document.getElementById("search_item_show");t.innerHTML="対象:"+e,t.value=e,t.style.display="",document.getElementById("search_item_value").value=e},search_post:h,check_and_fetch:async function(e){let t=document.getElementById("search_item_show"),n=document.getElementById("search_item_value"),o=document.getElementById("search_str"),a=document.getElementById("post_list"),s="";""===n.value&&(s+=" 検索対象項目 "),""===o.value&&(s+=" 検索文字列 "),s?alert(`${s}は必須です`):(t.innerHTML="中...",a.innerHTML='<div class="row"><div class="spinner-border text-success mx-auto text-center" role="status" id = "loading"><span class="visually-hidden">Loading...</span></div></div>',e=(e=e.replace("sheet_from",n.value)).replace("where",o.value),a.innerHTML=await h(e))},init_fetch:async function(e){let t=document.getElementById("post_list"),n=document.getElementById("search_item_show"),o=document.getElementById("search_item_value"),a=document.getElementById("search_str");n.innerHTML="",o.innerHTML="",o.value="",a.value="",t.innerHTML='<div class="row"><div class="spinner-border text-success mx-auto text-center" role="status" id = "loading"><span class="visually-hidden">Loading...</span></div></div>',t.innerHTML=await h(e)}},y=g;async function h(e){let t=await fetch(e);return await t.text()}const p={init:function(e){p.STATIC_URL=e;let t=document.getElementById("loading");window.onload=async function(){t.style="visibility:visible";let n=parseInt(document.getElementById("month").textContent),o=parseInt(document.getElementById("year").textContent),a=document.getElementsByTagName("table")[0],s=e.replace("month",n).replace("year",o).replace("status","active"),d=await fetch(s),c=await d.text();a.innerHTML=c,t.style="visibility:hidden"},document.getElementById("calendar-check").addEventListener("click",(()=>{f("z")})),document.getElementById("select-company").addEventListener("change",(()=>{f("s")}))},get_calendar:f,new_task:function(e){document.querySelector("select").addEventListener("change",(t=>{!function(t){if(0===t.target.selectedIndex)return;const n=t.target.selectedOptions[0];Main.default.open_as_window.open_as_window(e.replace("placeholder",n.value),"new_task_tab",500,1e3)}(t)})),document.getElementById("search-field").addEventListener("change",(()=>{const e=document.getElementById("search-field"),t=document.getElementById("choices").children;for(const n of t)n.innerText.includes(e.value)?n.hidden=!1:n.hidden=!0})),document.getElementById("button-addon").addEventListener("click",(()=>{document.getElementById("search-field").value="";const e=document.getElementById("choices").children;for(const t of e)t.hidden=!1}))},STATIC_URL:""};async function f(e){let t=p.STATIC_URL;loading.style="visibility:visible";let n=document.getElementById("month"),o=document.getElementById("year"),a=parseInt(document.getElementById("month").textContent),s=parseInt(document.getElementById("year").textContent),d=document.getElementById("select-company").selectedOptions[0].value,c=document.getElementById("calendar-check"),i="deactive";"n"==e?1<=a&&a<12?a+=1:(a=1,s+=1):"s"==e||"z"==e?0!=d&&(t=t.replace("search",d)):"b"==e&&(1<a&&a<=12?a-=1:(a=12,s-=1)),n.textContent=a,o.textContent=s,c.checked||(i="active");let l=document.getElementsByTagName("table")[0];t=t.replace("month",a).replace("year",s).replace("status",i),"0"!=d&&(t=t.replace("search",d));let r=await fetch(t),m=await r.text();l.innerHTML=m,loading.style="visibility:hidden"}const E={init:async function(e){const t=document.getElementById("id_choices");v("init",e),t.addEventListener("change",(()=>{v(t.value,e)}))},get_ticket:v,get_detail:async function(e,t){const n=E.selected;for(let e=0;e<n.length;e++){const e=E.selected.pop(),t=document.getElementById(e.id);t.style="",t.className=e.className}const o=document.getElementById("tr_"+e);o.style="background-color:#fccaf9 ",E.selected.push({id:`tr_${e}`,className:o.className}),o.className="selected";let a=document.getElementById("form_"+e);const s={method:"POST",body:new FormData(a)},d=await fetch(t,s),c=await d.text();document.getElementById("support_detail").innerHTML=c},change_is_solved:async function(e,t){let n=document.getElementById("form_"+e);const o={method:"POST",body:new FormData(n)};(await fetch(t,o)).ok&&window.location.reload()},selected:[]};async function v(e,t){const n=document.getElementById("support_table");n.innerHTML='<div class="row"><div class="spinner-border text-success mx-auto text-center" role="status" id = "loading"><span class="visually-hidden">Loading...</span></div></div>',t=t.replace("holder",e);let o=await fetch(t),a=await o.text();n.innerHTML=a}const w={t_save:I,init:function(){let e=document.getElementById("auto-save-check");e.addEventListener("click",(()=>{e.checked?function(){const e=document.getElementById("status-toast");e.className="toast bg-success";const t=bootstrap.Toast.getOrCreateInstance(e);document.getElementById("toast-status").innerHTML="自動保存が有効化されました",t.show();const n=document.getElementById("time-toast");n.className="toast bg-info";const o=bootstrap.Toast.getOrCreateInstance(n);document.getElementById("time-toast-status").innerHTML="最後に自動保存された時刻が表示されます",o.show(),w.id_autosave=setInterval((()=>{I(!0)}),3e4)}():b()}))},open_window:function(e,t,n,o){return window.open(`${e}`,`${t}`,`width=${n},height=${o},toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes`),!0},id_autosave:"initialized"};async function I(e){const t=document.getElementById("ESmodel-form").action,n=document.getElementById("ESmodel-form"),o=new FormData(n);let a,s,d=document.getElementById("status-toast"),c=bootstrap.Toast.getOrCreateInstance(d);const i={method:"POST",body:o};try{a=await fetch(t,i),s=await a.json()}catch{if("initialized"!=w.id_autosave){const e=document.getElementById("time-toast"),t=bootstrap.Toast.getOrCreateInstance(e);e.className="toast bg-danger",document.getElementById("auto-save-check").checked=!1,b(),t.show()}d.className="toast bg-danger",document.getElementById("toast-status").innerHTML="保存に失敗しました。ネットワーク接続を確認してください。",c.show()}"OK"==s.is_saved?!1===e?(d=document.getElementById("status-toast"),d.className="toast bg-info",c=bootstrap.Toast.getOrCreateInstance(d),document.getElementById("toast-status").innerHTML=`保存しました  保存時刻${s.saved_time.slice(0,8)}`,c.show()):document.getElementById("time-toast-status").innerHTML=`最終保存時刻: ${s.saved_time.slice(0,8)}`:(d=document.getElementById("status-toast"),d.className="toast bg-danger",c=bootstrap.Toast.getOrCreateInstance(d),document.getElementById("auto-save-check").checked=!1,b(),document.getElementById("toast-status").innerHTML=`保存に失敗しました。 <br> 理由:  ${s.errors}`,c.show())}function b(){clearInterval(w.id_autosave);const e=document.getElementById("status-toast");e.className="toast bg-secondary";const t=bootstrap.Toast.getOrCreateInstance(e);document.getElementById("toast-status").innerHTML="自動保存が無効化されました",t.show();const n=document.getElementById("time-toast");bootstrap.Toast.getOrCreateInstance(n).hide()}function B(e,t){let n="";return n+="\n----------\n",n+=`登録日時: ${t}\n`,n+=`タイトル: ${e.title}\n`,n+=`タグ: ${e.tag}\n`,n+=`詳細: ${e.desc}\n`,n+="<<<ここにメモを記入してください>>>\n",n+="----------\n",n}async function _(e){let t=document.getElementsByClassName("selectData"),n=[];for(const e of t)e.checked&&n.push(e.value);let o=document.getElementById("ESForm"),a=new FormData(o);a.append("selected_data",JSON.stringify(n));let s=await fetch(e,{method:"POST",body:a});if(s.ok){let e=await s.json(),t=e.sets,n=window.opener.document.getElementById("id_note");for(let o=0;o<t.length;o++)n.value+=B(t[o],e.date);alert(e.message),window.location.reload()}else alert("エラーが発生しました。ネットワークを確認してください")}const T={apply_extension:{main:function(e,t){let n=document.createElement("form");n.action=e,n.method="post";let o=document.createElement("input");o.name="csrfmiddlewaretoken",o.type="hidden",o.value=t,n.appendChild(o),document.body.appendChild(n),n.submit()}},signup_done:{d:function(){window.confirm("メールの送信を行わないと、アカウントの有効化が行われません。この画面は再度表示できることができませんがよろしいですか？")&&window.parent.document.location.reload()}},assist_tooltip:{main:async function(){const e=document.getElementById("assist-check");let t,n;e.addEventListener("change",(function(){e.checked?(t=document.querySelectorAll('[data-bs-toggle="tooltip"]'),n=[...t].map((e=>new bootstrap.Tooltip(e))),console.log("assisted")):(n.forEach((e=>e.dispose())),console.log("not assisted"))}));const o=await a.e(139).then(a.bind(a,139)),s=document.getElementsByClassName("form-control");for(let e=0;e<s.length;e++)s[e].setAttribute("data-bs-toggle","tooltip"),s[e].setAttribute("data-bs-placement","top"),s[e].setAttribute("data-bs-title",o.desc[s[e].name])}},edit_post:d,infomation:{conf_infomation:function(e,t,n,o){let a=document.createElement("form");a.action=n,a.method="post";let s=document.createElement("input");s.name="csrfmiddlewaretoken",s.type="hidden",s.value=o,a.appendChild(s);let d=document.createElement("input");d.type="hidden",d.name="id",d.value=e,a.appendChild(d);let c=document.createElement("input");c.type="hidden",c.name="operation",c.value=t,a.appendChild(c),document.body.appendChild(a),a.submit()}},interview_create:{init:function(){window.addEventListener("beforeunload",(function(){}))},search_zipcode:function(e){let t=document.getElementById("id_zipcode").value;if(t.length<7)return void alert("入力値を確認してください");let n=e.replace("placeholder",t);wind3=window.open(`${n}`,"get_address","width=400,height=400,toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes")},get_interviewer:async function(e){let t=await fetch(e,{method:"get"}),n=await t.json();"OK"==n.status?document.getElementById("id_interviewer").value=n.interviewer:document.body.innerHTML=n.res},get_address_from_sheet:async function(e){if(confirm("「企業データ」シート内の所在地の情報を取得します。面談録内の住所が上書きされますがよろしいですか？")){const t={method:"get"};let n=await fetch(e,t),o=await n.json();"OK"==o.status?(document.getElementById("id_place").value=o.location,document.getElementById("id_zipcode").value=o.postal_code):document.body.innerHTML=o.res}}},interview_main:{init:function(){window.addEventListener("beforeunload",(function(){}))},view_interview:function(e,t){let n=e.replace("placeholder",t);wind4=window.open(`${n}`,"view_interview"+t,"width=500,height=700,toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes")}},interview:l,interviewer:{p_save:async function(){const e=document.querySelector("form"),t=e.action;let n;const o={method:"POST",body:new FormData(e)},a=await fetch(t,o),s=await a.json();if(a.ok){console.log(s.status);const e=document.getElementById("status-toast");"OK"==s.status?("registered"===s.reason&&(window.location.href=s.redirect_to),e.className="toast bg-info",n=bootstrap.Toast.getOrCreateInstance(e),document.getElementById("toast-status").innerHTML=`保存しました 情報: ${s.reason}`,n.show()):"ERROR"==s.status?(e.className="toast bg-danger",n=bootstrap.Toast.getOrCreateInstance(e),document.getElementById("toast-status").innerHTML=`保存に失敗しました。  理由:  ${s.reason}  <br>エラー項目: ${s.error_list}`,n.show()):document.body.innerHTML=s.reason}else{const e=document.getElementById("status-toast");e.className="toast bg-danger",n=bootstrap.Toast.getOrCreateInstance(e),document.getElementById("toast-status").innerHTML=`保存に失敗しました。  理由:  ${a.statusText}`,n.show()}},init:function(){window.addEventListener("DOMContentLoaded",(()=>{document.querySelector("form").onsubmit=()=>(t_save(),!1)}))}},search_interviewer:{init:function(){let e=document.getElementsByName("button-addons");for(const t of e)window.opener.location.pathname.includes("view_interview")||t.children[1].children["button-addon-1"].remove()},addon:function(e){window.opener.document.getElementById("id_interviewer").value=e}},open_as_window:c,open_url:{open_url:function(e,t,n){let o,a=document.getElementById("id_prof_url").value;if(URL.canParse(a))i.open_as_window(document.getElementById("id_prof_url").value,e,t,n);else{const e=document.getElementById("status-toast");e.className="toast bg-danger",o=bootstrap.Toast.getOrCreateInstance(e),document.getElementById("toast-status").innerHTML="表示に失敗しました<br>http または https から始まるURLを入力してください",o.show()}}},search:g,signup:{init:function(){document.querySelector("form").addEventListener("submit",(function(e){confirm("ユーザー名・卒業年度は修正できませんがよろしいですか？")||e.preventDefault()}))}},mypage:{init:function(e){document.addEventListener("DOMContentLoaded",(async function(){await y.init_fetch(e)}))}},get_address:{init:function(e){document.addEventListener("DOMContentLoaded",(e=>{document.querySelectorAll('input[type=radio][name="address"]').forEach((e=>{e.addEventListener("change",(e=>{if(e.target.checked){let t=e.target.nextElementSibling.querySelector("#address").value;window.opener.document.getElementById("id_place").value=t}}))}))}))}},delete_post:{init:function(){document.getElementById("delete-button").addEventListener("click",(()=>{if(!confirm("注意！削除した情報は復元できません。本当に削除しますか？"))return!1;document.forms[0].submit()}))}},view_my_post:{change_active:function(e,t,n){let o=document.createElement("form");o.method="post",o.action=e;let a=document.getElementsByName("csrfmiddlewaretoken")[0];o.appendChild(a);let s=document.createElement("input");s.value=t,a.type="hidden",s.name="RegistID",o.appendChild(s);let d=document.createElement("input");d.value=n,d.type="hidden",d.name="current_status",o.appendChild(d),document.body.appendChild(o),o.submit()}},calc:{apply_calc:function(){var e=document.getElementById("capital"),t=document.getElementById("sales"),n=document.getElementById("salary"),o=document.getElementById("1"),a=document.getElementById("2"),s=document.getElementById("3"),d=o.value,c=a.value,i=s.value,l=0;e.checked?(l=Number(1e4*d)+Number(c),window.opener.document.getElementById("id_capital").value=l):t.checked?(l=Number(1e4*d)+Number(c),window.opener.document.getElementById("id_sales_n").value=l):n.checked&&(l=Number(1e4*d*1e4)+Number(1e4*c)+Number(1e3*i),window.opener.document.getElementById("id_salary").value=l)}},calendar_main:p,custom_sheet_create:{change_input:function(e){let t=document.getElementById(e+"_field_name");t.disabled?t.disabled=!1:t.disabled=!0},submit_sheet_settings:function(e){let t=document.querySelector("form"),n=document.getElementsByName("csrfmiddlewaretoken")[0];t.appendChild(n);let o=document.createElement("input");o.value=e,o.name="request_type",t.appendChild(o),t.method="post",t.submit()}},cat_interview:{init:function(){document.getElementById("choice").addEventListener("change",(()=>{const e=function(e){const t=document.createElement("div");return t.appendChild(document.createTextNode(e)),t.innerHTML}(document.getElementById("choice").selectedOptions[0].value);window.location.href=e}))}},footer:{init:function(){Main.default&&void 0!==Main.default.version&&(document.getElementById("js_version").innerText=`Library version:  ${Main.default.version}`)}},support:E,ManagementInfomation:{init:function(){const e=document.getElementById("infomation-addon"),t=document.createElement("button");t.onclick=()=>{let e=document.getElementById("search-holder"),t=document.getElementById("search-select");e.value="",t.selectedIndex=0;let n=document.getElementsByName("data-rows");for(const e of n)e.hidden=!1},t.className="btn btn-secondary",t.innerText="元に戻す";const n=document.createElement("button");n.onclick=()=>{if(0==document.getElementById("search-select").selectedIndex||""==document.getElementById("search-holder").value)return;let e=document.getElementsByName("data-rows");for(const t of e){let e=document.getElementById("search-holder"),n=document.getElementById("search-select");t.children[n.value].innerText.includes(e.value)||(t.hidden=!0)}document.getElementById("search-holder").value="",document.getElementById("search-select").selectedIndex=0},n.className="btn btn-success",n.innerText="絞り込む",e.appendChild(n),e.appendChild(t)}},ESmanage:{delete:{init:function(){let e=document.getElementsByClassName("form-control");for(let t=0;t<e.length;t++)e[t].disabled=!0;document.getElementById("id_tag").disabled=!0}},show:{search:async function(e){let t=document.getElementById("post_list");if(t.innerHTML='<div class="row"><div class="spinner-border text-success mx-auto text-center" role="status" id = "loading"><span class="visually-hidden">Loading...</span></div></div>',0==document.getElementById("search_str").value.length)return void alert("検索文字列を入力してください");const n=e.replace("placeholder",document.getElementById("search_str").value);let o=await fetch(n),a=await o.text();t.innerHTML=a},init:async function(e){let t=document.getElementById("post_list");t.innerHTML='<div class="row"><div class="spinner-border text-success mx-auto text-center" role="status" id = "loading"><span class="visually-hidden">Loading...</span></div></div>';let n=await fetch(e),o=await n.text();t.innerHTML=o,document.getElementById("search_str").value=""}},detail:w},ESdata:{get_detail:async function(e){let t=document.getElementById("ES_detail");t.innerHTML='<div class="row"><div class="spinner-border text-success mx-auto text-center" role="status" id = "loading"><span class="visually-hidden">Loading...</span></div></div>';let n=await fetch(e),o=await n.text();t.innerHTML=o;let a=document.getElementsByClassName("form-control");for(let e=0;e<a.length;e++)a[e].disabled=!0;document.getElementById("id_tag").disabled=!0},save_check:_,all_clear:async function(e){let t=document.getElementById("ESForm"),n=document.createElement("input");n.type="hidden",n.name="all_clear",t.appendChild(n),await _(e)}},Index:{init:function(){const e=document.body.scrollHeight;document.getElementById("data-frame").addEventListener("load",(function(){let t=document.getElementById("data-frame"),n=(document.getElementById("content"),document.getElementById("menubar")),o=document.getElementById("infobar"),a=(t.contentDocument||t.contentWindow.document).body.scrollHeight;t.style.height=a<e?e+"px":a+"px",e<a+o.scrollHeight+10?n.style.height=a+o.scrollHeight+10+"px":n.style.height=e+o.scrollHeight+"px"})),document.getElementById("data-frame").addEventListener("DOMContentLoaded",(()=>{console.log("changed")}))},loadContent:function(e){document.getElementById("first-show").hidden=!0;let t=document.getElementById("data-frame");t.hidden=!1,t.src=e}},version:"2.8.6"};Main=s})();