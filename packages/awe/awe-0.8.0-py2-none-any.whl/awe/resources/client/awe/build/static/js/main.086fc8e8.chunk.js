(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{167:function(e,t,n){e.exports=n(391)},387:function(e,t,n){},391:function(e,t,n){"use strict";n.r(t);var r=n(1),a=n.n(r),i=n(9),s=n.n(i),o=n(75),c=n(15),l=n(16),u=n(25),p=n(24),d=n(26),v=n(164),h=n.n(v),f=n(165),b=n.n(f),y=n(74),m=n.n(y),O=n(71),g=n.n(O),j=n(166),k=n.n(j),w=n(108),x=n.n(w),E=n(76),I=n(155),S=n.n(I),C=function(e){function t(){return Object(c.a)(this,t),Object(u.a)(this,Object(p.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props.table,t=e.data,n=t.headers,r=t.rows,i=n.map(function(e){return{title:e,dataIndex:e,key:e}}),s=r.map(function(e){var t=e.data,r=e.id,a=t.map(function(e,t){return[n[t],e]}),i={key:r},s=!0,o=!1,c=void 0;try{for(var l,u=a[Symbol.iterator]();!(s=(l=u.next()).done);s=!0){var p=l.value,d=Object(E.a)(p,2),v=d[0],h=d[1];i[v]=h}}catch(f){o=!0,c=f}finally{try{s||null==u.return||u.return()}finally{if(o)throw c}}return i});return a.a.createElement(S.a,Object.assign({},e.props,{dataSource:s,columns:i}))}}]),t}(r.Component),T=n(57),V=function(e){function t(){return Object(c.a)(this,t),Object(u.a)(this,Object(p.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props.grid,t=e.props,n=e.data,r=e.children;delete t.key;for(var i=n.columns,s=n.childColumns,o=24/i,c=[],l=[],u=0,p=0;p<r.length;p++){var d=p.toString(),v=r[p],h=o*s[p];u+h>24&&(c.push(l),u=0,l=[]),u+=h,l.push(a.a.createElement(T.Col,Object.assign({},t,{key:d,span:h}),v))}l.length>0&&c.push(l);var f=t.gutter||0;return c.map(function(e,n){return a.a.createElement(T.Row,Object.assign({},t,{key:n.toString(),style:{paddingBottom:f}}),e)})}}]),t}(r.Component),A=function(e){function t(){return Object(c.a)(this,t),Object(u.a)(this,Object(p.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props.text,t=e.data,n=e.props,r=(t.text||"").split("\n");return a.a.createElement("div",null,r.map(function(e,t){return e?a.a.createElement("div",Object.assign({},n,{key:t.toString()}),e):a.a.createElement("br",{key:t.toString()})}))}}]),t}(r.Component),M=n(160),J=n(161),P=n.n(J),D=n(106),W=n.n(D),B=n(162),F=n.n(B);function R(e){if(e.userOptions.callbackOptions.movingWindow){var t=function(t,n){var r=e.xAxis[0],a=r.getExtremes().dataMax,i=r.minRange;r.setExtremes(a-i,a+8e3,n)};t(0,!0),W.a.addEvent(e,"update",t)}}var N=function(e){function t(){return Object(c.a)(this,t),Object(u.a)(this,Object(p.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){for(var e=this.props.chart.data,t=e.data,n=e.options,r=e.movingWindow,i=[],s=Object.values(t),o=0;o<s.length;o++){var c=s[o],l=c.series,u=c.title,p=c.type,d={callbackOptions:{movingWindow:r},chart:{type:p,height:300},title:{text:u},plotOptions:Object(M.a)({},p,{marker:{enabled:!1,symbol:"circle"}}),time:{useUTC:!1},xAxis:{minRange:r?1e3*r:void 0,type:"datetime"},yAxis:{title:{text:""},tickPixelInterval:36}},v=void 0;Object.keys(n||{}).length>0?(P.a.defaultsDeep(n,[d]),v=n):v=d,v.series=l,i.push(v)}return a.a.createElement("div",null,i.map(function(e,t){return a.a.createElement(F.a,{callback:R,key:t.toString(),highcharts:W.a,options:e})}))}}]),t}(r.Component),G=n(107),U=n.n(G),q=n(163),z=null,H=function(){function e(t){var n=this,r=t.processor,a=t.host,i=t.port;Object(c.a)(this,e),this.processor=r,this.finishedInitialFetch=!1,this.pendingActions=[],this.ws=new WebSocket("ws://".concat(a,":").concat(i)),this.ws.onmessage=this.onMessage.bind(this),this.ws.onerror=function(e){return console.error("ws error",e)},e.fetchInitialState().then(function(e){n.processor.processInitialState(e);var t=e.version,r=!0,a=!1,i=void 0;try{for(var s,o=n.pendingActions[Symbol.iterator]();!(r=(s=o.next()).done);r=!0){var c=s.value;c.version>t&&n.processor.dispatch(c)}}catch(l){a=!0,i=l}finally{try{r||null==o.return||o.return()}finally{if(a)throw i}}n.pendingActions=[],n.finishedInitialFetch=!0})}return Object(l.a)(e,[{key:"call",value:function(e,t){this.sendMessage({type:"call",functionId:e,kwargs:t})}},{key:"updateVariable",value:function(e,t){this.sendMessage({type:"updateVariable",variableId:e,value:t})}},{key:"sendMessage",value:function(e){this.ws.send(JSON.stringify(e))}},{key:"onMessage",value:function(e){var t=JSON.parse(e.data);this.finishedInitialFetch?this.processor.dispatch(t):this.pendingActions.push(t)}}],[{key:"start",value:function(t){var n=t.processor,r=t.host,a=void 0===r?"127.0.0.1":r,i=t.port;return z=new e({processor:n,host:a,port:void 0===i?9e3:i})}},{key:"fetchInitialState",value:function(){var e=Object(q.a)(U.a.mark(function e(){return U.a.wrap(function(e){for(;;)switch(e.prev=e.next){case 0:return e.next=2,fetch("/initial-state");case 2:return e.next=4,e.sent.json();case 4:return e.abrupt("return",e.sent);case 5:case"end":return e.stop()}},e,this)}));return function(){return e.apply(this,arguments)}}()}]),e}(),K={div:function(e){return a.a.createElement("div",e.props,e.children)}},L={Text:function(e){return a.a.createElement(A,Object.assign({},e.props,{text:e}))},Card:function(e){return a.a.createElement(h.a,e.props,e.children.length>0?e.children:e.data.text)},Table:function(e){return a.a.createElement(C,Object.assign({},e.props,{table:e}))},Grid:function(e){return a.a.createElement(V,Object.assign({},e.props,{grid:e}))},Divider:function(e){return a.a.createElement(b.a,e.props)},Collapse:function(e){return a.a.createElement(x.a,e.props,e.children)},Panel:function(e){return a.a.createElement(x.a.Panel,e.props,e.children)},Tab:function(e){return a.a.createElement(m.a.TabPane,e.props,e.children)},Tabs:function(e){return a.a.createElement(m.a,e.props,e.children||a.a.createElement("div",null))},Button:function(e){return a.a.createElement(g.a,Object.assign({},e.props,{onClick:function(){return z.call(e.id)}}),e.data.text)},Input:function(e){return a.a.createElement(k.a,Object.assign({},e.props,{value:e.variables[e.id].value,onChange:function(t){return e.updateVariable(e.id,t.target.value)},onPressEnter:function(){return e.data.enter?z.call(e.id):null}}))},Chart:function(e){return a.a.createElement(N,Object.assign({},e.props,{chart:e}))}},Q=Object.assign({},K,L);n(387);function X(e){return e.children=e.children.map(X),Q[e.elementType](e)}var Y=function(e){function t(){return Object(c.a)(this,t),Object(u.a)(this,Object(p.a)(t).apply(this,arguments))}return Object(d.a)(t,e),Object(l.a)(t,[{key:"render",value:function(){var e=this.props.state.toJS(),t=e.elements,n=e.variables,r=e.style,a=this.props.updateVariable,i=Object.values(t).sort(function(e,t){return e.index-t.index}),s={elementType:"div",children:[],props:{style:r}},o=!0,c=!1,l=void 0;try{for(var u,p=i[Symbol.iterator]();!(o=(u=p.next()).done);o=!0){var d=u.value;d.variables=n,d.updateVariable=a,(t[d.parentId]||s).children.push(d)}}catch(v){c=!0,l=v}finally{try{o||null==p.return||p.return()}finally{if(c)throw l}}return X(s)}}]),t}(r.Component),Z=Object(o.b)(function(e){return{state:e}},function(e){return{updateVariable:function(t,n){e({type:"updateVariable",id:t,value:n}),z.updateVariable(t,n)}}})(Y),$=function(){function e(t){Object(c.a)(this,e),this.store=t}return Object(l.a)(e,[{key:"processInitialState",value:function(e){var t=e.variables,n=e.children,r=e.style,a=e.title;this.processTitle(a),this.processStyle(r);for(var i=Object.values(t),s=0;s<i.length;s++){var o=i[s];this.processVariable(o)}var c=!0,l=!1,u=void 0;try{for(var p,d=n[Symbol.iterator]();!(c=(p=d.next()).done);c=!0){var v=p.value;this.processElement(v)}}catch(h){l=!0,u=h}finally{try{c||null==d.return||d.return()}finally{if(l)throw u}}}},{key:"processTitle",value:function(e){document.title=e}},{key:"processStyle",value:function(e){this.dispatch({type:"setStyle",style:e})}},{key:"processVariable",value:function(e){var t=e.id,n=e.value,r=e.version;this.dispatch({type:"newVariable",id:t,value:n,version:r})}},{key:"processElement",value:function(e){var t=e.children,n=e.data,r=e.elementType,a=e.index,i=e.id,s=e.parentId,o=e.props;if(this.dispatch({type:"newElement",id:i,elementType:r,index:a,data:n,parentId:s,props:o}),t){var c=!0,l=!1,u=void 0;try{for(var p,d=t[Symbol.iterator]();!(c=(p=d.next()).done);c=!0){var v=p.value;v.parentId=i,this.processElement(v)}}catch(h){l=!0,u=h}finally{try{c||null==d.return||d.return()}finally{if(l)throw u}}}}},{key:"dispatch",value:function(e){this.store.dispatch(e)}}]),e}(),_=n(42),ee=n(72),te=Object(_.a)({elements:{},variables:{},style:{}});var ne={append:function(e){return function(t){return t.push(e)}},prepend:function(e){return function(t){return t.unshift(e)}},addChartData:function(e){return function(t){return t.withMutations(function(t){var n=!0,r=!1,a=void 0;try{for(var i,s=e.values()[Symbol.iterator]();!(n=(i=s.next()).done);n=!0){var o=i.value,c=o.get("title"),l={},u=!0,p=!1,d=void 0;try{for(var v,h=o.get("series").values()[Symbol.iterator]();!(u=(v=h.next()).done);u=!0){var f=v.value;l[f.get("name")]=f.get("data")}}catch(A){p=!0,d=A}finally{try{u||null==h.return||h.return()}finally{if(p)throw d}}var b=[c,"series"],y=t.getIn(b),m=!0,O=!1,g=void 0;try{for(var j,k=y.entries()[Symbol.iterator]();!(m=(j=k.next()).done);m=!0){var w=j.value,x=Object(E.a)(w,2),I=x[0],S=x[1],C=S.get("data"),T=l[S.get("name")],V=C.concat(T);y=y.set(I,S.set("data",V)),t=t.setIn(b,y)}}catch(A){O=!0,g=A}finally{try{m||null==k.return||k.return()}finally{if(O)throw g}}}}catch(A){r=!0,a=A}finally{try{n||null==s.return||s.return()}finally{if(r)throw a}}return t})}}};var re,ae={setStyle:function(e,t){var n=t.style;return e.set("style",n)},newElement:function(e,t){var n=t.id,r=t.index,a=t.data,i=t.parentId,s=t.elementType,o=t.props,c=void 0===o?{}:o;return e.setIn(["elements",n],Object(_.a)({index:r,id:n,parentId:i,data:a,elementType:s,props:c,children:[]}))},newVariable:function(e,t){var n=t.id,r=t.value,a=t.version;return e.setIn(["variables",n],Object(_.a)({id:n,value:r,version:a}))},updateElement:(re="elements",function(e,t){var n=t.id,r=t.updateData,a=r.path,i=void 0===a?[]:a,s=r.action,o=r.data,c=[re,n].concat(i);return"set"===s?e.setIn(c,Object(_.a)(o)):e.updateIn(c,ne[s](Object(_.a)(o)))}),updateVariable:function(e,t){var n=t.id,r=t.value,a=t.version,i=void 0===a?-1:a,s=-1===i,o=e.getIn(["variables",n,"version"]);if(!s&&o>=i)return e;var c={value:r};return s||(c.version=i),e.mergeIn(["variables",n],Object(_.a)(c))}};var ie=Object(ee.b)(function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:te,t=arguments.length>1?arguments[1]:void 0,n=ae[t.type];return n?n(e,t):e});H.start({processor:new $(ie)}),s.a.render(a.a.createElement(o.a,{store:ie},a.a.createElement(Z,null)),document.getElementById("root"))}},[[167,2,1]]]);
//# sourceMappingURL=main.086fc8e8.chunk.js.map