const modal=document.getElementById('modal'),mt=document.getElementById('mt'),mb=document.getElementById('mb');
const copy={
home:['Human · Systems · Performance','Tres disciplinas. Una misma forma de pensar. Personas, procesos, tecnología y rendimiento conectados en un único sistema profesional.'],
profile:['Mi perfil','Integro dirección de operaciones y eventos, sistemas y transformación digital, y entrenamiento y rendimiento bajo una misma metodología de análisis, ejecución y mejora continua.'],
experience:['Experiencia','Hostelería aporta liderazgo operativo y servicio; Tecnología aporta sistemas, datos y automatización; Deporte aporta evaluación, planificación y progresión.'],
method:['Metodología','Analizar → Diseñar → Ejecutar → Medir → Mejorar.'],
projects:['Proyectos','Chetesaí Fitness+, Portfolio IT, OpoStudy, Farmagend y proyectos de Hospitality representan distintas aplicaciones de la misma visión profesional.'],
contact:['Contacto','Accede a mis portfolios especializados o conecta conmigo desde los enlaces del panel.'],
'Planificación':['Planificación','Objetivos, cronograma, recursos, responsables, riesgos y criterios de éxito.'],
'Recursos':['Recursos','Personas, presupuesto, proveedores, infraestructura y capacidades.'],
'Ejecución':['Ejecución','Coordinación operativa con foco en calidad, tiempos, experiencia y resultado.'],
'Monitoreo':['Monitoreo','KPI, calidad, tiempos e incidencias para decidir con información.'],
'Cierre':['Cierre','Resultados, consumos, aprendizaje y acciones de mejora.'],
'Desarrollo':['Desarrollo','Soluciones web, automatización e integración de herramientas.'],
'Sistemas':['Sistemas','Infraestructura, administración y arquitectura de sistemas.'],
'Redes':['Redes','Conectividad, servicios y administración de redes.'],
'Seguridad':['Seguridad','Ciberseguridad, hardening, riesgo y buenas prácticas.'],
'IA & Data':['IA & Data','Datos e inteligencia artificial para analizar y automatizar.'],
'Automatización':['Automatización','Procesos más eficientes, reproducibles y medibles.'],
'Sueño':['Sueño','Recuperación y descanso dentro del sistema de rendimiento.'],
'Fuerza':['Fuerza','Progresión, técnica y control de carga.'],
'Recuperación':['Recuperación','Balance entre estímulo, descanso y adaptación.'],
'Movimiento':['Movimiento','Actividad diaria, salud y hábito.'],
'Nutrición':['Nutrición','Estrategia nutricional adaptada al objetivo.'],
'Energía':['Energía','Disponibilidad y gestión de la carga.'],
'Frecuencia cardíaca':['Frecuencia cardíaca','Contexto de recuperación y respuesta al esfuerzo.'],
'Estrés':['Estrés','Recuperación mental y sostenibilidad del rendimiento.'],
'Seguimiento':['Seguimiento','Medición del avance, incidencias y resultados.'],
'Optimización':['Optimización','Corregir, simplificar, automatizar y elevar el sistema.'],
'Personas':['Personas','Liderazgo, comunicación, experiencia y desarrollo.'],
'Procesos':['Procesos','Estructura reproducible para convertir objetivos en ejecución.'],
'Resultados':['Resultados','Evidencia, KPI, calidad, experiencia y aprendizaje.'],
'Hostelería':['Hostelería','F&B, eventos, logística, equipos, costes y experiencia de cliente.'],
'Tecnología':['Tecnología','Sistemas, desarrollo, redes, seguridad, IA y automatización.'],
'Deporte':['Deporte','Entrenamiento, nutrición, hábitos, recuperación y rendimiento.']
};
function openInfo(key){const d=copy[key]||[key,'Área integrada en mi enfoque profesional.'];mt.textContent=d[0];mb.textContent=d[1];modal.showModal()}
document.querySelectorAll('[data-open]').forEach(b=>b.onclick=()=>openInfo(b.dataset.open));
document.querySelectorAll('[data-info]').forEach(b=>b.onclick=()=>openInfo(b.dataset.info));
document.querySelectorAll('[data-project]').forEach(b=>b.onclick=()=>{mt.textContent=b.dataset.project;mb.textContent='Proyecto multidisciplinar conectado con estrategia, sistemas y mejora continua.';modal.showModal()});
document.querySelector('.close').onclick=()=>modal.close();modal.onclick=e=>{if(e.target===modal)modal.close()};