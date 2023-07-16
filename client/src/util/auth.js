
export function saveAuthToken(token){
    localStorage.setItem('token', token);
    return token;
}

export function getAuthToken(){
    const token = localStorage.getItem('token');
    return token;
}

export function tokenLoader(){
    return getAuthToken();
}