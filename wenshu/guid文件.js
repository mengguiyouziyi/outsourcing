function Getguid() {
    var createGuid = function () {
        return (((1 + Math.random()) * 65536) | 0).toString(16).substring(1)
    }
    var guid = createGuid() + createGuid() + "-" + createGuid() + "-" + createGuid() + createGuid() + "-" + createGuid() + createGuid() + createGuid();
    // console.log(guid)
    return guid
}

// Getguid()