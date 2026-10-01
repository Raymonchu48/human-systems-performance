const dialog=document.getElementById('infoDialog');
const title=document.getElementById('dialogTitle');
const body=document.getElementById('dialogBody');
const kicker=document.getElementById('dialogKicker');
const actions=document.getElementById('dialogActions');

const copy={
profile:['MI PERFIL','Perfil multidisciplinar','Integro más de dos décadas de experiencia profesional con dirección de operaciones y eventos, tecnología, sistemas, entrenamiento, nutrición y gestión de proyectos. Mi enfoque conecta personas, procesos, tecnología y rendimiento.'],
experience:['EXPERIENCIA','Tres mundos, una misma lógica','Hostelería me aporta dirección operativa, servicio y liderazgo; Tecnología aporta sistemas, datos y automatización; Deporte aporta planificación, evaluación y mejora progresiva. Los tres ámbitos comparten metodología, coordinación y orientación a resultados.'],
method:['METODOLOGÍA','Analizar · Diseñar · Ejecutar · Medir · Mejorar','Trabajo desde una lógica de sistema: entender el contexto, diseñar una solución, coordinar recursos, medir resultados y mejorar de forma continua. La misma metodología se aplica a un evento, una plataforma digital o un programa de rendimiento.'],
projects:['PROYECTOS','Proyectos multidisciplinares','Chetesaí Fitness+, Farmagend, OpoStudy, Portfolio IT, Portfolio Deportivo y proyectos de Hospitality representan distintas aplicaciones de una misma visión profesional.'],
contact:['CONTACTO','Conectemos','Puedes explorar mis portfolios especializados y mi CV completo desde este portfolio maestro.'],
home:['HUMAN · SYSTEMS · PERFORMANCE','Tres disciplinas. Una misma forma de pensar.','No veo áreas aisladas. Veo sistemas formados por personas, procesos, información, tecnología y objetivos.']
};

const detailCopy={
'Planificación':'Definir objetivos, cronograma, recursos, responsables, riesgos y criterios de éxito.',
'Recursos':'Dimensionar personas, materiales, proveedores, infraestructura, presupuesto y capacidades.',
'Ejecución':'Coordinar la operación en tiempo real y mantener el estándar de servicio o entrega.',
'Monitoreo':'Controlar KPI, tiempos, calidad, incidencias y experiencia para tomar decisiones rápidas.',
'Cierre':'Consolidar resultados, consumos, incidencias, aprendizaje y acciones de mejora.',
'Desarrollo':'Diseño y construcción de soluciones web, automatizaciones y herramientas aplicadas.',
'Sistemas':'Infraestructura, administración, integración y visión de arquitectura de sistemas.',
'Redes':'Conectividad, administración de redes, servicios y resolución de incidencias.',
'Seguridad':'Seguridad informática, hardening, análisis de riesgos y buenas prácticas.',
'IA & Data':'Uso de datos e inteligencia artificial para analizar, automatizar y mejorar decisiones.',
'Automatización':'Transformar tareas repetitivas y procesos en flujos más eficientes y medibles.',
'Sueño':'Recuperación y descanso como parte del sistema de rendimiento.',
'Fuerza':'Progresión estructurada, técnica, adaptación y control de carga.',
'Recuperación':'Equilibrio entre estímulo, descanso, movilidad y adaptación.',
'Movimiento':'Actividad diaria como indicador de salud, hábito y rendimiento.',
'Nutrición':'Estrategia nutricional adaptada al objetivo, contexto y adherencia.',
'Energía':'Gestión de carga, disponibilidad y percepción de esfuerzo.',
'Frecuencia cardíaca':'Métrica útil para contextualizar recuperación y respuesta al esfuerzo.',
'Estrés':'Gestión del entorno, recuperación mental y sostenibilidad del rendimiento.',
'Personas':'Las personas son el núcleo: liderazgo, comunicación, experiencia, formación y desarrollo.',
'Procesos':'Los procesos convierten objetivos en sistemas reproducibles y coordinados.',
'Resultados':'Los resultados se evalúan mediante evidencia, KPI, calidad, experiencia y aprendizaje.',
'Planificación':'Definir objetivos, recursos, prioridades y una ruta de ejecución clara.',
'Seguimiento':'Medir avance, incidencias y resultados con indicadores relevantes.',
'Optimización':'Corregir, simplificar, automatizar y elevar el rendimiento del sistema.'
};

function show(k,t,b,links=[]){
 kicker.textContent=k; title.textContent=t; body.textContent=b; actions.innerHTML='';
 links.forEach(x=>{const a=document.createElement('a');a.href=x.href;a.target='_blank';a.rel='noreferrer';a.textContent=x.label;actions.appendChild(a)});
 dialog.showModal();
}
document.querySelectorAll('[data-open]').forEach(el=>el.addEventListener('click',()=>{
 const d=copy[el.dataset.open]||copy.home;
 const links=el.dataset.open==='profile'?[{label:'CV completo',href:'https://raw.githubusercontent.com/Raymonchu48/Portfolio/main/Resumen_CV-2026.pdf'}]:el.dataset.open==='contact'?[{label:'Portfolio IT',href:'https://raymonchu48.github.io/Portfolio/'},{label:'Portfolio Deportivo',href:'https://raymonchu48.github.io/Deportivo/'}]:[];
 show(d[0],d[1],d[2],links);
}));
document.querySelectorAll('[data-detail]').forEach(el=>el.addEventListener('click',()=>show('HUMAN · SYSTEMS · PERFORMANCE',el.dataset.detail,detailCopy[el.dataset.detail]||'Área integrada dentro de mi enfoque profesional.')));
document.querySelectorAll('[data-step]').forEach(el=>el.addEventListener('click',()=>show('MI METODOLOGÍA',el.dataset.step,detailCopy[el.dataset.step]||copy.method[2])));
document.querySelectorAll('[data-project]').forEach(el=>el.addEventListener('click',()=>show('PROYECTO',el.dataset.project,'Proyecto seleccionado por representar la integración entre estrategia, operaciones, tecnología y mejora continua.')));
document.querySelectorAll('[data-domain]').forEach(el=>el.addEventListener('click',e=>{if(e.target.closest('button,a')!==el&&el.tagName!=='BUTTON')return;const d=el.dataset.domain;if(d==='hospitality')show('HOSTELERÍA','Dirección · Operaciones · Experiencia','F&B, banquetes, eventos, logística, equipos, servicio, costes, KPI y experiencia del cliente.');if(d==='technology')show('TECNOLOGÍA','Systems · Development · Automation','Sistemas, redes, desarrollo, ciberseguridad, datos, inteligencia artificial y transformación digital.');if(d==='sport')show('DEPORTE','Movimiento · Salud · Rendimiento','Entrenamiento, nutrición, recuperación, hábitos, coaching y evaluación orientados al rendimiento sostenible.')}));

document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close()});
const menu=document.querySelector('.menu-btn'),nav=document.querySelector('.topnav');
menu.addEventListener('click',()=>{const o=nav.classList.toggle('open');menu.setAttribute('aria-expanded',o)});
