'use strict';

// rozklad.kpi.ua/Schedules/ViewSchedule.aspx?g=26d47cdd-5e07-4c1a-9ae1-0ff5f5ceced9
// http://rozklad.kpi.ua/Schedules/ScheduleGroupSelection.aspx
//.reduce((first, second) => first.concat(second), [])
//(?<=a)
//USE telegram-mtproto?

let data = '';

const http = require('http');
const qs = require('querystring');
const fs = require('fs');

// const options = {
//     // headers: req.headers,
//     host: 'rozklad.kpi.ua',
//     method: 'GET',
//     path: '/Schedules/ViewSchedule.aspx?g=26d47cdd-5e07-4c1a-9ae1-0ff5f5ceced9',
//     timeout: 40000
// };

const options = {
    // headers: req.headers,
    host: 'rozklad.kpi.ua',
    method: 'GET',
    path: '/Schedules/ScheduleGroupSelection.aspx',
    timeout: 40000
};

const parseTT = data => {
    // console.log('\x1b[33m=========================================================================================================\x1b[0m');
    // console.log(data);
    let weeks = data.split('table table-bordered table-hover').map(weeks => weeks.split('</tr>'));//get weeks array, consisting of arrays of lessons 1-5
    weeks.shift();
    weeks = weeks.map(lessonPos => lessonPos.map(lesson => lesson.split('</td>')));
    weeks.map(week => {
        week.pop();
        week.shift();
    });//remove trash from beginning and end
    weeks = weeks.reduce((first, second) => first.concat(second), []);//get array with 10 lesson arrays - 1st week 1-5 then 2nd week 1-5, each split into strings for each day mon-fri
    weeks = weeks.map(lesson => {
        lesson.pop();
        lesson.shift();
        return lesson;
    });//remove trash from beginning and end
    weeks = weeks.map(lesson => lesson.map(day => {
        let lesData = day.split('<a class="plainLink" ');
        lesData = lesData.map(data => data.slice(0, data.indexOf('</a>')).replace('>', ' '));
        let les = {
            lessonLink: '',
            lesson: '',
            teacherLink: '',
            teacher: '',
            classroomLink: '',
            classroom: '',
        };
        if (lesData.length === 2) {//for P.E. only
            les.lessonLink = lesData[1].match(/href=".*?"/)[0].slice(6, -1);
            les.lesson = lesData[1].match(/title=".*"/)[0].slice(7, -1);
        } else if (lesData.length === 3) {//trash, lesson, room - no teacher!!!
            les.lessonLink = lesData[1].match(/href=".*?"/)[0].slice(6, -1);
            les.lesson = lesData[1].match(/title=".*"/)[0].slice(7, -1);
            les.classroomLink = lesData[lesData.length - 1].match(/href=".*"/)[0].slice(6, -1);
            les.classroom = lesData[lesData.length - 1].match(/" .*/)[0].slice(1);
        } else if (lesData.length !== 1) {//add extra teachers!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            //WHAT IF NO TEACHER???
            // console.log(lesData);
            les.lessonLink = lesData[1].match(/href=".*?"/)[0].slice(6, -1);
            les.lesson = lesData[1].match(/title=".*"/)[0].slice(7, -1);
            les.teacherLink = 'http://' + options.host + lesData[2].match(/href=".*?"/)[0].slice(6, -1);
            les.teacher = lesData[2].match(/title=".*"/)[0].slice(7, -1);
            les.classroomLink = lesData[lesData.length - 1].match(/href=".*"/)[0].slice(6, -1);
            les.classroom = lesData[lesData.length - 1].match(/" .*/)[0].slice(1);
        }//else this is a free les
        les.lessonLink = les.lessonLink.replace(/ /g, '_');
        les.lessonLink = les.lessonLink.replace(/\)/g, '%29');
        les.classroomLink = les.classroomLink.replace(/ /g, '');
        // console.log(les);
        // les.lessonLink = '';//while lesson link is dead on kpi.ua
        return les;
    }));
    // console.log(weeks);
    return weeks;
};

const parseTable = data => {
    let group;
    // console.log(process.argv);
    if (process.argv.length <= 2)
        group = 'іп-71';
    else
        group = process.argv[2]
    // console.log(group);
    let inputs = data.match(/<input .*?\/>/g);
    // console.log(inputs);
    inputs[4] = inputs[4].slice(0, -2) + 'value="' + group + '"/>';
    // console.log(inputs);
    let obj = {};
    inputs.map(input => {
        obj[input.match(/name=".*?"/)[0].slice(6, -1)] = input.match(/value=".*?"/g)[0].slice(7, -1);
        // console.log(input.match(/name=".*?"/)[0].slice(6, -1));
        // console.log(input.match(/value=".*?"/g)[0].slice(7, -1));
    });
    // console.log(obj);
    obj = qs.stringify(obj);
    // console.log(obj);
    return obj;
};

const makeRequest = (options) => {
    return new Promise((resolve, reject) => {
        let request = http.request(options, (response) => {
            response.setEncoding('utf8');
            response.on('data', (chunk) => {
                data += chunk;
            });

            response.on('close', () => {
                // console.log(data);
                // return data;
                resolve(data);
            })
        });

        request.on('timeout', () => {
            console.log('Request timeout');
        });

        request.on('error', e => {
            console.log('REQUEST ERROR:');
            console.log('\x1b[33mWARNING:\x1b[0m: ');
            console.log('\x1b[33mWARNING:\x1b[0m: ', e);
            reject(e);
        });

        request.write('GIMME');
        request.end();
    });
};

const getTT = async () => {
    let rawMainHtml = await makeRequest(options);//returns raw HTML
    let path = parseTable(rawMainHtml);
    options.path += '?';
    options.path += path;
    let rawResponse = await makeRequest(options);
    let regex = rawResponse.match(/(?<=<h2>.*?)<a href=.*?>/);
    if (regex) {
        options.path = regex[0].slice(9, -2);
        // console.log(options.path);
        let tt = await makeRequest(options);
        return parseTT(tt);
    } else return parseTT(data);
};

( async () => console.log(JSON.stringify(await getTT())) )();
