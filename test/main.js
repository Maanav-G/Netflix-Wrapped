function handleUserData() {
    const formData = new FormData();
    formData.append('timeFrame', "2020");


    const requestOptions = {
        method: 'POST',
        headers: { 
            "content-type": "application/json"
        },
        body: JSON.stringify("data")
        // body: formData,
    };
    fetch('https://xa19tzs2a5.execute-api.us-east-1.amazonaws.com/Prod', requestOptions)
        .then((response) => response.json())
        .then(function (data) {
            console.log(data);
        })
        .catch(function (error) {
            console.log(error);
        });
};
