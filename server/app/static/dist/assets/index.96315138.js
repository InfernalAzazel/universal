import{d as N,b as F,Q as H,r as h,R as A,A as s,h as T,z as v,w as o,S as B,n as t,l as u,j as f,B as $,t as j,v as l,U as G}from"./index.90662b97.js";import{u as J}from"./crud.6c5008af.js";const W=N({__name:"index",setup(I){const{t:e}=F(),x=H({label:e("crud.label"),addText:e("crud.addText"),detailText:e("crud.detailText"),editText:e("crud.editText"),searchText:e("crud.searchText"),searchResetText:e("crud.searchResetText"),submitText:e("crud.submitText"),resetText:e("crud.resetText"),detail:!0,edit:!0,del:!1,searchReset:!0,fixed:"right",width:"200"}),D=h([{value:"GET",label:"GET"},{value:"POST",label:"POST"},{value:"PUT",label:"PUT"},{value:"DELETE",label:"DELETE"}]),g=A([{label:e("system.interface.id"),prop:"id",component:"el-input",detail:!0,props:{disabled:!0}},{label:e("system.interface.path"),prop:"path",component:"el-input",form:!0,search:!0,detail:!0},{label:e("system.interface.group"),prop:"group",component:"el-input",form:!0,search:!0,detail:!0},{label:e("system.interface.describe_zh_cn"),prop:"describe_zh_cn",component:"el-input",form:!0,detail:!0},{label:e("system.interface.describe_en_us"),prop:"describe_en_us",component:"el-input",form:!0,detail:!0},{label:e("system.interface.method"),prop:"method",component:"pro-select",form:!0,search:!0,detail:!0,props:{data:D.value}},{label:e("el-date-picker.create_at"),prop:"create_at",component:"el-date-picker",props:{type:"datetimerange",rangeSeparator:"-",startPlaceholder:"start",endPlaceholder:"end",format:"YYYY-MM-DD",valueFormat:"YYYY-MM-DDTHH:mm:ss"},search:!0,detail:!0},{label:e("el-date-picker.update_at"),prop:"update_at",component:"el-date-picker",props:{type:"datetimerange",rangeSeparator:"-",startPlaceholder:"start",endPlaceholder:"end",format:"YYYY-MM-DD",valueFormat:"YYYY-MM-DDTHH:mm:ss"},search:!0,detail:!0}]),d=h(JSON.parse(JSON.stringify(g))),{form:i,serachForm:p,detail:S,loadList:b,currentPage:c,pageSize:m,list:Y,total:y,isFetching:w,beforeOpen:z,submit:C,search:k,deleteRow:E}=J(s.interfaceList,s.interfaceAdd,s.interfaceEdit,s.interfaceDelete,!0),M={path:{required:!0,message:e("rules.interface.path"),trigger:"blur"},group:{required:!0,message:e("rules.interface.group"),trigger:"blur"},describe_zh_cn:{required:!0,message:e("rules.interface.describe_zh_cn"),trigger:"blur"},describe_en_us:{required:!0,message:e("rules.interface.describe_en_us"),trigger:"blur"},method:{required:!0,message:e("rules.interface.method"),trigger:"blur"}};return(n,a)=>{const P=l("pro-column-setting"),R=l("el-button"),U=l("el-popconfirm"),V=l("pro-crud"),L=l("pro-card"),O=G("loading");return T(),v(L,null,{default:o(()=>[B((T(),v(V,{modelValue:t(i),"onUpdate:modelValue":a[1]||(a[1]=r=>u(i)?i.value=r:null),search:t(p),"onUpdate:search":a[2]||(a[2]=r=>u(p)?p.value=r:null),"current-page":t(c),"onUpdate:current-page":a[3]||(a[3]=r=>u(c)?c.value=r:null),"page-size":t(m),"onUpdate:page-size":a[4]||(a[4]=r=>u(m)?m.value=r:null),columns:t(g),menu:t(x),rules:M,data:t(Y),detail:t(S),"before-open":t(z),onSearch:t(k),onSubmit:t(C),"row-key":"key","table-columns":d.value,total:t(y),onLoad:t(b),onSearchReset:t(b),layout:"total, ->, jumper, prev, pager, next, sizes",border:"",stripe:"","show-overflow-tooltip":""},{action:o(()=>[f(P,{modelValue:d.value,"onUpdate:modelValue":a[0]||(a[0]=r=>d.value=r),"allow-drag":r=>n.console.log(r),"allow-drop":(r,_,q)=>n.console.log(r),"default-expand-all":"",icon:"SettingOutlined"},null,8,["modelValue","allow-drag","allow-drop"])]),menu:o(({row:r,size:_})=>[f(U,{title:n.$t("crud.isDelText"),onConfirm:q=>t(E)(r)},{reference:o(()=>[f(R,{size:_,type:"danger",link:""},{default:o(()=>[$(j(n.$t("crud.delText")),1)]),_:2},1032,["size"])]),_:2},1032,["title","onConfirm"])]),_:1},8,["modelValue","search","current-page","page-size","columns","menu","data","detail","before-open","onSearch","onSubmit","table-columns","total","onLoad","onSearchReset"])),[[O,t(w)]])]),_:1})}}});export{W as default};
