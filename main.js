// ============================================================
// КА-Строй — общий JS: мобильное меню, форма (Web3Forms), калькулятор
// ============================================================
(function(){
  // Мобильное меню
  var toggle=document.querySelector('.nav-toggle');
  var nav=document.querySelector('.nav');
  if(toggle&&nav){
    toggle.addEventListener('click',function(){
      nav.classList.toggle('is-open');
    });
  }
 
  // Помечаем активный пункт меню
  try{
    var path=location.pathname.replace(/\/+$/,'')||'/';
    var navLinks=document.querySelectorAll('.nav a');
    for(var i=0;i<navLinks.length;i++){
      var href=navLinks[i].getAttribute('href')||'';
      var hp=href.replace(/\/+$/,'')||'/';
      if(hp===path){navLinks[i].classList.add('is-active');}
    }
  }catch(e){}
 
  // Web3Forms — обработка отправки
  var form=document.querySelector('form[data-ks-form]');
  if(form){
    var statusEl=form.querySelector('.form-status');
    var submit=form.querySelector('button[type="submit"]');
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(statusEl){statusEl.className='form-status';statusEl.textContent='';}
      // Собираем выбранные услуги в hidden services
      var svcInputs=form.querySelectorAll('input[data-svc]:checked');
      var svc=[];for(var i=0;i<svcInputs.length;i++){svc.push(svcInputs[i].value);}
      var servicesField=form.querySelector('input[name="Интересующие услуги"]');
      if(!servicesField){
        servicesField=document.createElement('input');
        servicesField.type='hidden';
        servicesField.name='Интересующие услуги';
        form.appendChild(servicesField);
      }
      servicesField.value=svc.length?svc.join(', '):'(не указано)';
 
      if(submit){submit.disabled=true;submit.textContent='Отправляем…';}
 
      var fd=new FormData(form);
      fetch(form.getAttribute('action'),{
        method:'POST',
        body:fd,
        headers:{'Accept':'application/json'}
      }).then(function(r){return r.json();}).then(function(data){
        if(data.success){
          if(statusEl){statusEl.className='form-status ok';statusEl.textContent='Спасибо! Заявка отправлена. Мы свяжемся с вами в течение рабочего дня.';}
          form.reset();
        }else{
          if(statusEl){statusEl.className='form-status err';statusEl.textContent='Не удалось отправить форму. Позвоните нам: +7 (383) 311-02-02.';}
        }
      }).catch(function(){
        if(statusEl){statusEl.className='form-status err';statusEl.textContent='Не удалось отправить форму. Позвоните нам: +7 (383) 311-02-02.';}
      }).finally(function(){
        if(submit){submit.disabled=false;submit.textContent='Отправить заявку';}
      });
    });
  }
 
  // Плавный скролл по data-scroll
  var scrollLinks=document.querySelectorAll('a[data-scroll]');
  for(var j=0;j<scrollLinks.length;j++){
    (function(a){
      a.addEventListener('click',function(e){
        var sel=a.getAttribute('data-scroll');
        var t=document.querySelector('[data-anchor="'+sel+'"]');
        if(t){e.preventDefault();t.scrollIntoView({behavior:'smooth',block:'start'});}
      });
    })(scrollLinks[j]);
  }
 
  // Калькулятор
  var calc=document.querySelector('[data-calc]');
  if(calc){
    var prices={
      asfalt_b1:{name:'Асфальт ЩМА Б-I',unit:'т',price:5500},
      asfalt_b2:{name:'Асфальтобетонная смесь Б-II',unit:'т',price:5000},
      asfalt_drobl:{name:'Асфальтная крошка',unit:'т',price:1200},
      pesok:{name:'Песок (с доставкой)',unit:'м³',price:850},
      shps:{name:'ЩПС (щебёночно-песчаная смесь)',unit:'т',price:1100},
      schebеn:{name:'Щебень фр. 5-20',unit:'т',price:1300},
      asfalt_under_key:{name:'Асфальтирование под ключ (1–2 слоя)',unit:'м²',price:500},
      remont_yam:{name:'Ямочный ремонт',unit:'м²',price:850},
      blagoustr:{name:'Благоустройство',unit:'м²',price:1200},
      arenda_excav:{name:'Аренда экскаватора',unit:'смена',price:18000},
      arenda_kat:{name:'Аренда катка',unit:'смена',price:14000},
      arenda_uklad:{name:'Аренда асфальтоукладчика',unit:'смена',price:32000}
    };
    var sel=calc.querySelector('[data-calc-svc]');
    var qty=calc.querySelector('[data-calc-qty]');
    var resV=calc.querySelector('[data-calc-result]');
    var resS=calc.querySelector('[data-calc-sub]');
    var resU=calc.querySelector('[data-calc-unit]');
    function fmt(n){
      n=Math.round(n);
      return n.toString().replace(/\B(?=(\d{3})+(?!\d))/g,' ');
    }
    function calcResult(){
      var key=sel.value;
      var item=prices[key];
      if(!item){return;}
      var q=Math.max(0,parseFloat(qty.value)||0);
      if(resU)resU.textContent=item.unit;
      var total=q*item.price;
      if(resV)resV.textContent=fmt(total)+' ₽';
      if(resS)resS.textContent=item.name+' · '+fmt(item.price)+' ₽/'+item.unit;
    }
    if(sel&&qty){
      sel.addEventListener('change',calcResult);
      qty.addEventListener('input',calcResult);
      calcResult();
    }
  }
})();