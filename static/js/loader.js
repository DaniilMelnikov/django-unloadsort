function httpGet(theUrl)
        {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open("GET", theUrl, false);
            xmlHttp.send(null);
            return xmlHttp;
        }

function sendPocket(split)
        {
            for (let i = 0; i < split; i++){
                console.log(count);
                params = '?domain_json=' + domain + '&region=' + region + '&id=' + id + '&pocket=' + i + '&split=' + split + '&count=' + count;
                let res = httpGet('/validate/' + params);
                console.log(res);
            }
        }

let res = httpGet('/media/json/json_user.json');
let json_data = JSON.parse(res.response);
let id = 0;
for (var domain of Object.keys(json_data)) {
    id = 0;
    for (var region of Object.keys(json_data[domain])) {
        if (region == "count") {
            break;
        }
        count = Math.floor(Number(json_data[domain]['count'][id]));
        if (Number(json_data[domain]['count'][0]) < 50){
            sendPocket(1);
        } else {
            count /= 2;
            sendPocket(2);
        }
        id++;
    }
}

let write = httpGet('/write_results/');
console.log(write);

document.querySelector('.load').innerHTML = 'Файл загружен, перейдите на главную и нажмите кнопку для скачивания'
