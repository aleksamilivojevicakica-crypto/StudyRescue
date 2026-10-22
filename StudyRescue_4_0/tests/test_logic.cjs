'use strict';
const assert=require('assert');
const fs=require('fs'),vm=require('vm');
const root=__dirname+'/..';
const localeSource=fs.readFileSync(root+'/assets/translations.js','utf8');
const appSource=fs.readFileSync(root+'/assets/app.js','utf8').replace('setNav();configureDialog();render();','window.__TEST__={makePlan,priority,validTask,baseState,fallbackParse,samples,localKey,addDays,render};setNav();configureDialog();render();');
function environment(lang,page='overview',state=null){
 let nodes={};function node(id){return nodes[id] ||= {id,innerHTML:'',value:'',textContent:'',dataset:{},hidden:false,disabled:false,classList:{add(){},remove(){},toggle(){}},setAttribute(){},addEventListener(){},add(){},focus(){},setSelectionRange(){},reset(){},showModal(){},close(){}};}
 let store=state?JSON.stringify(state):null;
 let document={body:{dataset:{lang,page}},querySelector(s){return node(s);},querySelectorAll(){return [];},addEventListener(){},};
 let sandbox={window:{},document,localStorage:{getItem:()=>store,setItem(_key,v){store=v;}},console,Option:function(){},Date,Math,Number,Array,Object,JSON,Intl,String,RegExp,Map,Set,Promise,setTimeout,clearTimeout,setInterval,clearInterval,crypto:require('crypto').webcrypto};
 vm.createContext(sandbox);vm.runInContext(localeSource,sandbox);vm.runInContext(appSource,sandbox);return {api:sandbox.window.__TEST__,nodes,store:()=>store};
}
const en=environment('en'); assert(en.nodes['#pageContent'].innerHTML.includes('Less overwhelm'));
const de=environment('de');assert(de.nodes['#pageContent'].innerHTML.includes('Weniger Stress'));
const fr=environment('fr');assert(fr.nodes['#pageContent'].innerHTML.includes('Moins de stress'));
const tasks=environment('fr','tasks');assert(tasks.nodes['#pageContent'].innerHTML.includes('Tous tes devoirs'));
const settings=environment('de','settings');assert(settings.nodes['#pageContent'].innerHTML.includes('Verfügbarkeit'));
const today=en.api.localKey(new Date());
let st=en.api.baseState();st.availability=[0,0,0,0,0,0,0];
st.tasks=[{id:'one',title:'School project',subject:'cs',due:en.api.localKey(en.api.addDays(new Date(),1)),minutes:120,difficulty:3,importance:3,notes:'',done:false,created:1}];
const noTime=environment('en','planner',st);const plan=noTime.api.makePlan();assert.equal(plan.unscheduled.length,1);assert.equal(plan.unscheduled[0].minutes,120);assert(noTime.nodes['#pageContent'].innerHTML.includes('Workload warnings'));
let st2=en.api.baseState();st2.tasks=[{...st.tasks[0],due:en.api.localKey(en.api.addDays(new Date(),40))}];const future=environment('en','overview',st2);assert.equal(future.api.makePlan().unscheduled.length,0);assert.equal(future.api.makePlan().beyond.length,1);assert(future.nodes['#pageContent'].innerHTML.includes('outside the 21-day'));
assert.equal(en.api.fallbackParse('Math homework tomorrow 90 min').minutes,90);
assert.equal(de.api.fallbackParse('Mathe morgen 60 Minuten').subject,'math');
assert.equal(fr.api.fallbackParse('Projet biologie demain 45 min').subject,'science');
console.log('PASS: 3 languages, multiple pages, date-aware scheduling, overload, horizon and quick-add parsing');
