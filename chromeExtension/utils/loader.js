function startLoader() {
    console.log("loader.start()")
    document.getElementsByClassName("bd")[0].innerHTML = `
        <br/> <br/> <br/>
        <h3 style="text-align: center;">
            Fetching your viewing history... <br/>
            Please wait a few minutes!
        </h3>
    `
}
