
var q = 0

document.addEventListener('DOMContentLoaded', async () => {
    setInterval(checkFileOnServer, 6000);
    removeClickEventHandlers();
    // checkFileOnServer()
})

async function checkFileOnServer() {
    const response = await fetch(`http://127.0.0.1:8000/images?q=${q}`,{
        method:'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    if (response.ok){
        const blob = await response.blob();
        // 이미지가 아니면 크기가 작음
        if (blob.size < 10) {
            console.log('no image response')
        }
        else {
            handleResponse(blob, q);
            q += 1
        }

    } else {
        console.error('response error');
    }
}

function handleResponse(data, q) {
    makeImgTag(q)
    const imageUrl = URL.createObjectURL(data);
    // console.log(imageUrl)
    // console.log('여기다')
    document.getElementById(`img${q}`).src = imageUrl;

    console.log('받은 응답:', data); 
}

function makeImgTag(q) {
    const listBox = document.getElementById('list-box')
    const liTag = document.createElement('li')
    const imgTag = document.createElement('img')

    liTag.classList.add('img-mini-box')
    imgTag.id = `img${q}`
    imgTag.src = ""
    imgTag.alt = "" 

    liTag.appendChild(imgTag)
    listBox.appendChild(liTag)
    addClickEventHandlers();
}


// 이전에 등록된 클릭 이벤트 핸들러 삭제하는 함수
function removeClickEventHandlers() {
    const iTags = document.querySelectorAll('ul#list-box img');
    iTags.forEach(item => {
        item.removeEventListener('click', handleImageClick);
    });
}

// 새로운 이미지에 대한 클릭 이벤트 핸들러 등록하는 함수
function addClickEventHandlers() {
    const iTags = document.querySelectorAll('ul#list-box img');
    iTags.forEach(item => {
        item.addEventListener('click', handleImageClick);
    });
}

// 이미지 클릭 이벤트 핸들러
function handleImageClick(e) {
    getImgDetail(e.target.id.substring(3))
    console.log('클릭된 이미지의 id:', e.target.id);
}
// img0
async function getImgDetail(imgNo) {
    const response = await fetch(`http://127.0.0.1:8000/info?q=${imgNo}`,{
        method:'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    if (response.ok){
        response.json().then((data) => {
            // car img는 src긁어오기
            const ocr = data.OCR
            const perspective_dir = data.perspective_path
            const date = data.date

            handleDetailResponse(perspective_dir, date, ocr, imgNo);
        })
    } else {
        console.error('response error');
    }
}

function handleDetailResponse(perspective_dir, date, ocr, imgNo) {
    const subImg = document.querySelector('#sub-img')
    const plate = document.querySelector('#plate')
    const logBox = document.querySelector('.log-box')
    // const imageUrl = URL.createObjectURL(img);
    plate.src = false
    plate_box.textContent = ''

    subImg.src = getImgSrc(imgNo)
    console.log(perspective_dir)
    if (perspective_dir){
        plate.src = `http://127.0.0.1:8000/perspective?q=${perspective_dir}`
        if (ocr){
            plate_box.textContent = ocr
        }
    }else{
        const plate_box = document.getElementById('plate_box')
        plate_box.textContent = '번호판을 인식하지 못했습니다.'
    }
        
    
    day = date.split("_")[0]
    time = date.split("_")[1]
    hour = time.split("-")[0]
    minutes = time.split("-")[1]
    sec = time.split("-")[2]


    logBox.innerHTML = `
    <ul>
        <li>
            날짜
        </li>
        <li>
            ${day}
        </li>
    </ul>
    <ul>
        <li>
            시간
        </li>
        <li>
            ${hour}:${minutes}:${sec}
        </li>
    </ul>   
`
}


function getImgSrc(no) {
    return document.getElementById(`img${no}`).src

}
