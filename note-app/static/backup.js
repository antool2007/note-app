// 노트를 자동 저장하는 함수
function autoSave() {
    const notes = document.getElementById("notes").value.split("\n");

    fetch("/save_notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ notes: notes })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            console.log("노트 저장 완료");
        } else {
            console.error("노트 저장 실패:", data);
        }
    })
    .catch(error => {
        console.error("노트 저장 중 오류 발생:", error);
    });
}

// 백업 버튼 클릭 시 백업 요청 및 애니메이션 처리
function backupNotes() {
    const notes = document.getElementById("notes").value.split("\n");

    // 버튼 클릭 시 애니메이션 적용
    const saveButton = document.querySelector('.save-btn');
    saveButton.style.transform = 'scale(0.1)'; // 10%까지 작아짐
    setTimeout(() => {
        saveButton.style.transform = 'scale(1)'; // 원래 크기로 복귀
    }, 300); // 300ms 후 원래 크기로 복귀

    fetch("/backup_notes", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ notes: notes })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "backup success") {
            console.log("백업 완료: " + data.filename);
        }
    })
    .catch(error => {
        console.error("백업 중 오류 발생:", error);
    });
}
