module.exports = {
    deepCopyIfNeeded,
    deepCopy
};

function deepCopyIfNeeded(resource/*obj|array|str*/, returnSafeRef=false/*Boolean,Default=false*/) {
    console.log(returnSafeRef);
    if (returnSafeRef !== undefined && 
        typeof returnSafeRef !== 'boolean') {
        throw new Error(`secAag's input error:returnSafeRef(secArg) can be ignored, otherwise, ` + 
            `must be boolean value\(true, false\)!` + 
            `\nYour secArg is: ${returnSafeRef}`);
    } else if (!returnSafeRef) {
        return resource;
    }

    return deepCopy(resource);
}

function deepCopy(obj) {
    if (obj === undefined) {
        return ;
    }
    return JSON.parse(JSON.stringify(obj));
}
