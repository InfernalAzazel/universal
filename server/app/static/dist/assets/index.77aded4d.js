import{d as v,C as y,e as a,q as o,w as l,g as c,y as p,i as n,f as C,E as b,F as g,G as x,H as k,n as i,s as S,t as h}from"./index.305d1985.js";const E=v({__name:"index",props:{modelValue:{type:String,default:""},data:{type:[Array,Object],default:[]}},emits:["update:modelValue"],setup(s,{emit:m}){const f=s,{modelValue:t}=y(f),_=u=>{m("update:modelValue",u)};return(u,r)=>{const d=i("el-icon"),V=i("el-option");return a(),o(n(k),{modelValue:n(t),"onUpdate:modelValue":r[0]||(r[0]=e=>x(t)?t.value=e:null),placeholder:"Select",onChange:_},{prefix:l(()=>[c(d,{size:20},{default:l(()=>[(a(),o(p(n(t))))]),_:1})]),default:l(()=>[(a(!0),C(g,null,b(s.data,e=>(a(),o(V,{key:e.value,label:e.label,value:e.value},{default:l(()=>[c(d,{size:20},{default:l(()=>[(a(),o(p(e.label)))]),_:2},1024),S(" "+h(e.label),1)]),_:2},1032,["label","value"]))),128))]),_:1},8,["modelValue"])}}});export{E as default};