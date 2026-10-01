const areaButtons=document.querySelectorAll('[data-area]');
const panels=document.querySelectorAll('[data-panel]');
const dialog=document.getElementById('detailDialog');
const dialogTitle=document.getElementById('dialogTitle');
const dialogBody=document.getElementById('dialogBody');
const dialogEyebrow=document.getElementById('dialogEyebrow');
const methodCopy=document.getElementById('methodCopy');

const areaCopy={
  hospitality:{eyebrow:'HOSTELERÍA',title:'Operaciones y experiencia',body:'La hostelería me ha enseñado a gestionar personas, servicio, logística y resultados en tiempo real. Aquí el sistema funciona cuando cada detalle, cada equipo y cada proceso converge en una experiencia coherente y rentable.'},
  tech:{eyebrow:'TECNOLOGÍA',title:'Sistemas y transformación digital',body:'La tecnología me permite convertir procesos en sistemas medibles, automatizables y escalables: infraestructura, software, datos, ciberseguridad e inteligencia artificial al servicio de objetivos reales.'},
  sport:{eyebrow:'DEPORTE',title:'Rendimiento humano',body:'El deporte aporta la lógica de la progresión: evaluar, programar, ejecutar, medir y ajustar. Rendimiento, nutrición, hábitos y coaching integrados con una visión técnica y humana.'}
};

function openDialog(eyebrow,title,body){
  dialogEyebrow.textContent=eyebrow;
  dialogTitle.textContent=title;
  dialogBody.textContent=body;
  dialog.showModal();
}

areaButtons.forEach(btn=>btn.addEventListener('click',()=>{
  const key=btn.dataset.area;
  const data=areaCopy[key];
  panels.forEach(p=>p.classList.toggle('active',p.dataset.panel===key));
  openDialog(data.eyebrow,data.title,data.body);
}));

document.querySelectorAll('[data-open]').forEach(btn=>btn.addEventListener('click',()=>{
  const type=btn.dataset.open;
  if(type==='profile'){
    openDialog('PERFIL PROFESIONAL','Tres disciplinas. Una misma forma de pensar.','Mi trayectoria integra dirección y operaciones en hostelería, sistemas y transformación digital, y entrenamiento y rendimiento. El hilo conductor es el mismo: personas, procesos, información, tecnología y mejora continua.');
  }else{
    openDialog('LA CONEXIÓN','People × Processes × Technology × Performance','No veo áreas aisladas. Veo sistemas. Las personas generan valor, los procesos dan estructura, la tecnología amplifica capacidades y la medición convierte la experiencia en aprendizaje y rendimiento.');
  }
}));

document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});

const methodTexts={
  Analizar:'Entender contexto, necesidades, recursos, personas y restricciones antes de tomar decisiones.',
  Diseñar:'Convertir el análisis en estructura: procesos, arquitectura, estrategia, experiencia y prioridades.',
  Ejecutar:'Coordinar personas, herramientas y recursos con claridad operativa y foco en el resultado.',
  Medir:'Transformar actividad en evidencia mediante KPI, datos, rendimiento, calidad y experiencia.',
  Mejorar:'Iterar con criterio: corregir, automatizar, simplificar y elevar de forma continua el sistema.'
};
document.querySelectorAll('[data-step]').forEach(btn=>btn.addEventListener('click',()=>{
  document.querySelectorAll('[data-step]').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  methodCopy.textContent=methodTexts[btn.dataset.step];
}));

document.querySelectorAll('[data-project]').forEach(btn=>btn.addEventListener('click',()=>{
  openDialog('PROYECTO',btn.dataset.project,btn.querySelector('span').textContent+'. Proyecto seleccionado por representar una parte concreta de la integración entre estrategia, sistemas, experiencia y rendimiento.');
}));

const menuBtn=document.querySelector('.menu-btn');
const nav=document.querySelector('.nav');
menuBtn.addEventListener('click',()=>{
  const open=nav.classList.toggle('open');
  menuBtn.setAttribute('aria-expanded',open);
});