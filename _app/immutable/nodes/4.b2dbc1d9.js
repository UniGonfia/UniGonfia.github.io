${l.target.value}`),S.append("title").text(l=>`${l.source.name} → ${l.target.name}
${l.target.value}`),_.append("g").selectAll().data(b).join("text").attr("x",l=>l.x0<s/2?l.x1-40:l.x0+40).attr("y",l=>(l.y1+l.y0)/2).attr("dy","0.35em").attr("text-anchor",l=>l.x0<s/2?"end":"start").attr("fill","wheat").text(l=>l.name)}return se(async()=>{a()}),[]}class je extends ue{constructor(a){super(),oe(this,a,Ke,Re,le,{})}}export{je as component,qe as universal};