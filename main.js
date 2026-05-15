// ============================================================
// КА-Строй — общий JS: мобильное меню, форма (Web3Forms), калькулятор
// ============================================================
(function(){
  // Стрелки для ленты популярных материалов
  try{
    var tracks=document.querySelectorAll('.hero-ribbon-track');
    for(var t=0;t<tracks.length;t++){
      (function(track){
        var ribbon=track.querySelector('.hero-ribbon');
        var prev=track.querySelector('[data-ribbon-prev]');
        var next=track.querySelector('[data-ribbon-next]');
        if(!ribbon||!prev||!next)return;
        function step(){var card=ribbon.querySelector('.hero-ribbon__card');return card?card.offsetWidth+14:240;}
        function update(){
          var max=ribbon.scrollWidth-ribbon.clientWidth-2;
          if(ribbon.scrollLeft<=0){prev.setAttribute('disabled','');}else{prev.removeAttribute('disabled');}
          if(ribbon.scrollLeft>=max){next.setAttribute('disabled','');}else{next.removeAttribute('disabled');}
        }
        prev.addEventListener('click',function(){ribbon.scrollBy({left:-step(),behavior:'smooth'});});
        next.addEventListener('click',function(){ribbon.scrollBy({left:step(),behavior:'smooth'});});
        ribbon.addEventListener('scroll',update,{passive:true});
        window.addEventListener('resize',update);
        setTimeout(update,80);
      })(tracks[t]);
    }
  }catch(e){}

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

  // Маска и валидация телефона
  function phoneMask(input){
    input.addEventListener('input',function(){
      var val=input.value.replace(/\D/g,'');
      if(val.length===0){input.value='';return;}
      if(val[0]==='8')val='7'+val.slice(1);
      if(val[0]!=='7')val='7'+val;
      var out='+7';
      if(val.length>1)out+=' ('+val.slice(1,4);
      if(val.length>4)out+=') '+val.slice(4,7);
      if(val.length>7)out+='-'+val.slice(7,9);
      if(val.length>9)out+='-'+val.slice(9,11);
      input.value=out;
    });
    input.addEventListener('keydown',function(e){
      if(e.key==='Backspace'&&input.value.length<=3){
        e.preventDefault();input.value='';
      }
    });
    input.addEventListener('focus',function(){
      if(!input.value)input.value='+7';
    });
    input.addEventListener('blur',function(){
      if(input.value==='+7'||input.value==='+7 ')input.value='';
    });
  }
  function isValidPhone(val){
    var digits=val.replace(/\D/g,'');
    return digits.length===11&&digits[0]==='7';
  }
  var phoneInputs=document.querySelectorAll('input[type="tel"]');
  for(var pi=0;pi<phoneInputs.length;pi++){phoneMask(phoneInputs[pi]);}

  // Web3Forms — обработка отправки
  var form=document.querySelector('form[data-ks-form]');
  if(form){
    var statusEl=form.querySelector('.form-status');
    var submit=form.querySelector('button[type="submit"]');
    form.addEventListener('submit',function(e){
      e.preventDefault();
      if(statusEl){statusEl.className='form-status';statusEl.textContent='';}
      var phoneField=form.querySelector('input[type="tel"]');
      if(phoneField&&!isValidPhone(phoneField.value)){
        if(statusEl){statusEl.className='form-status err';statusEl.textContent='Введите корректный номер телефона.';}
        phoneField.focus();return;
      }
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
 
  // Callback modal (плашка «Заказать звонок» в шапке)
  var cbModal=document.querySelector('[data-callback-modal]');
  if(cbModal){
    var opens=document.querySelectorAll('[data-callback-open]');
    var closes=cbModal.querySelectorAll('[data-callback-close]');
    var cbForm=cbModal.querySelector('[data-callback-form]');
    var cbStatus=cbModal.querySelector('.callback-modal__status');
    var cbSubmit=cbModal.querySelector('.callback-modal__submit');
    function openModal(){
      cbModal.removeAttribute('hidden');
      cbModal.classList.add('is-open');
      document.body.style.overflow='hidden';
      var firstInput=cbForm&&cbForm.querySelector('input[type="text"],input[type="tel"]');
      if(firstInput){setTimeout(function(){firstInput.focus();},80);}
    }
    function closeModal(){
      cbModal.classList.remove('is-open');
      cbModal.setAttribute('hidden','');
      document.body.style.overflow='';
    }
    for(var k=0;k<opens.length;k++){
      opens[k].addEventListener('click',function(e){e.preventDefault();openModal();});
    }
    for(var m=0;m<closes.length;m++){
      closes[m].addEventListener('click',function(e){e.preventDefault();closeModal();});
    }
    document.addEventListener('keydown',function(e){
      if(e.key==='Escape'&&cbModal.classList.contains('is-open')){closeModal();}
    });
    if(cbForm){
      cbForm.addEventListener('submit',function(e){
        e.preventDefault();
        if(cbStatus){cbStatus.className='callback-modal__status';cbStatus.textContent='';}
        var cbPhone=cbForm.querySelector('input[type="tel"]');
        if(cbPhone&&!isValidPhone(cbPhone.value)){
          if(cbStatus){cbStatus.className='callback-modal__status err';cbStatus.textContent='Введите корректный номер телефона.';}
          cbPhone.focus();return;
        }
        if(cbSubmit){cbSubmit.disabled=true;cbSubmit.textContent='Отправляем…';}
        var fd=new FormData(cbForm);
        fetch(cbForm.getAttribute('action'),{
          method:'POST',body:fd,headers:{'Accept':'application/json'}
        }).then(function(r){return r.json();}).then(function(data){
          if(data.success){
            if(cbStatus){cbStatus.className='callback-modal__status ok';cbStatus.textContent='Спасибо! Перезвоним в течение 15 минут.';}
            cbForm.reset();
            setTimeout(closeModal,2200);
          }else{
            if(cbStatus){cbStatus.className='callback-modal__status err';cbStatus.textContent='Не удалось отправить. Позвоните: +7 (383) 311-02-02.';}
          }
        }).catch(function(){
          if(cbStatus){cbStatus.className='callback-modal__status err';cbStatus.textContent='Не удалось отправить. Позвоните: +7 (383) 311-02-02.';}
        }).finally(function(){
          if(cbSubmit){cbSubmit.disabled=false;cbSubmit.textContent='Заказать звонок';}
        });
      });
    }
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