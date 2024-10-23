// Meeting List Fetch
document.addEventListener('DOMContentLoaded', function () {
    // Fetch meeting list when the meeting list page loads
    if (document.getElementById('meetingList')) {
        fetch('/meetings')
            .then(response => response.json())
            .then(data => {
                let tableBody = document.getElementById('meetingList');
                data.forEach(meeting => {
                    let row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${meeting.id}</td>
                        <td>${meeting.topic}</td>
                        <td>${meeting.date}</td>
                        <td>${meeting.start_time}</td>
                        <td>${meeting.end_time}</td>
                        <td>${meeting.participants}</td>
                        <td>
                            <button onclick="location.href='edit_meeting.html?id=${meeting.id}'">Update</button>
                            <button onclick="deleteMeeting(${meeting.id})">Delete</button>
                        </td>
                    `;
                    tableBody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching meeting list:', error));
    }

    // Edit Meeting Fetch
    const urlParams = new URLSearchParams(window.location.search);
    const meetingId = urlParams.get('id');
    if (meetingId && document.getElementById('editMeetingForm')) {
        fetch(`/meetings/${meetingId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(meeting => {
                document.getElementById('meetingId').value = meeting.id;
                document.getElementById('topic').value = meeting.topic;
                document.getElementById('date').value = meeting.date;
                document.getElementById('start_time').value = meeting.start_time;
                document.getElementById('end_time').value = meeting.end_time;
                document.getElementById('participants').value = meeting.participants;
            })
            .catch(error => console.error('Error fetching meeting:', error));
    }
});

// Add Meeting
document.getElementById('addMeetingForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    const newMeeting = {
        topic: document.getElementById('topic').value,
        date: document.getElementById('date').value,
        start_time: document.getElementById('start_time').value,
        end_time: document.getElementById('end_time').value,
        participants: document.getElementById('participants').value
    };

    fetch('/meetings', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newMeeting)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = 'meeting_list.html';
    })
    .catch(error => console.error('Error adding meeting:', error));
});

// Edit Meeting
document.getElementById('editMeetingForm')?.addEventListener('submit', function (e) {
    e.preventDefault();
    const meetingId = document.getElementById('meetingId').value;
    const updatedMeeting = {
        topic: document.getElementById('topic').value,
        date: document.getElementById('date').value,
        start_time: document.getElementById('start_time').value,
        end_time: document.getElementById('end_time').value,
        participants: document.getElementById('participants').value
    };

    fetch(`/meetings/${meetingId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedMeeting)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        window.location.href = 'meeting_list.html';
    })
    .catch(error => console.error('Error updating meeting:', error));
});

// Delete Meeting
function deleteMeeting(meetingId) {
    if (confirm('Are you sure you want to delete this meeting?')) {
        fetch(`/meetings/${meetingId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
            window.location.reload();
        })
        .catch(error => console.error('Error deleting meeting:', error));
    }
}
