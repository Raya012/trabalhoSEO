(function(){
  var K="cds_carrinho", P="";
  function ler(){try{return JSON.parse(localStorage.getItem(K))||{}}catch(e){return {}}}
  function gravar(c){try{localStorage.setItem(K,JSON.stringify(c))}catch(e){}}
  function total(c){return Object.keys(c).reduce(function(s,k){return s+c[k]},0)}
  function brl(v){return "R$ "+v.toFixed(2).replace(".",",")}
  function contador(){var n=total(ler());document.querySelectorAll("[data-cart-count]").forEach(function(e){e.textContent=n})}
  function acha(s){return (window.CATALOGO||[]).filter(function(p){return p.slug===s})[0]}
  function esc(t){var d=document.createElement("div");d.textContent=t;return d.innerHTML}
  document.querySelectorAll("[data-add]").forEach(function(b){b.addEventListener("click",function(){
    var c=ler(),s=b.getAttribute("data-add");c[s]=(c[s]||0)+1;gravar(c);contador();
    var a=document.querySelector("[data-added]");if(a)a.hidden=false;});});
  var box=document.getElementById("carrinho-itens");
  if(box){(function draw(){var c=ler(),ks=Object.keys(c);if(!ks.length){box.className="caixa vazio";box.innerHTML="<p>Nenhum item.</p>";return}
    var t=0;box.className="caixa";box.innerHTML=ks.map(function(s){var p=acha(s);if(!p)return "";t+=p.preco*c[s];
      return "<p>"+esc(p.nome)+" × "+c[s]+" — "+brl(p.preco*c[s])+' <button type="button" data-rm="'+s+'">Remover</button></p>'}).join("")+"<p><strong>Total: "+brl(t)+"</strong></p>";
    box.querySelectorAll("[data-rm]").forEach(function(b){b.addEventListener("click",function(){var c=ler();delete c[b.getAttribute("data-rm")];gravar(c);contador();draw()})});})();}
  var res=document.getElementById("busca-resultados");
  if(res){var q=(new URLSearchParams(location.search).get("q")||"").trim().toLowerCase();var r=document.getElementById("busca-resumo");
    if(q){var f=(window.CATALOGO||[]).filter(function(p){return p.nome.toLowerCase().indexOf(q)>-1});
      r.textContent=f.length?f.length+" resultado(s) para “"+q+"”.":"Nenhum resultado para “"+q+"”.";
      res.innerHTML=f.map(function(p){return '<article class="caixa card"><img src="'+p.img+'" alt="'+esc(p.alt)+'" width="480" height="320" loading="lazy"><h2>'+esc(p.nome)+'</h2><p class="preco">'+brl(p.preco)+'</p><a href="'+p.url+'">Ver detalhes: '+esc(p.nome.toLowerCase())+'</a></article>'}).join("")}}
  contador();
})();
