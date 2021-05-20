'use strict'

//sessionStorage.setItem('flag', 'true');


function urlB64ToUnit8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/\-/g, '+')
        .replace(/_/g, '/');

    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    const outputData = outputArray.map((output, index) => rawData.charCodeAt(index));

    return outputData;
}


const registerSw = async () => {
    if ('serviceWorker' in navigator) {
        const reg = await navigator.serviceWorker.register("/sw.js", {scope: "/"});
        
        initialiseState(reg)

    } else {
        alert("You can't send push notifications ☹️😢");
    }
};


const initialiseState = (reg) => {
    if (!reg.showNotification) {
        return
    }
    if (Notification.permission === 'denied') {
        return
    }
    if (Notification.permission === 'default') {
        
        //return
    }
    if (!'PushManager' in window) {
        return
    }
    
    //console.log(Notification.permission)

    subscribe(reg);
}

const subscribe = async (reg) => {
    const subscription = await reg.pushManager.getSubscription();
    if (subscription) {
        //console.log(subscription)
        sendSubData(subscription);
        return;
    }

    const vapidMeta = document.querySelector('meta[name="vapid-key"]');
    const key = vapidMeta.content;
    const options = {
        userVisibleOnly: true,
        // if key exists, create applicationServerKey property
        ...(key && {applicationServerKey: urlB64ToUnit8Array(key)})
    };
    //console.log(options)
    const sub = await reg.pushManager.subscribe(options);

    sendSubData(sub)
};

const sendSubData = async (subscription) => {
    //console.log(subscription)
    const browser = navigator.userAgent.match(/(firefox|msie|chrome|safari|trident)/ig)[0].toLowerCase();
    const data = {
        status_type: 'subscribe',
        subscription: subscription.toJSON(),
        browser: browser,
    };
    
    //console.log(data)
    //if (!sessionStorage.getItem('flag')) {
    console.log(sessionStorage.getItem('flag'))
    const res = await fetch('/index/save-information', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: {
            'content-type': 'application/json'
        },
        credentials: "include"
    });

    handleResponse(res);
    //}
};

const handleResponse = (res) => {
    /*sessionStorage.setItem('flag', 'false');
    console.log(res.status);
    console.log(sessionStorage.getItem('flag'))*/
};

registerSw();
