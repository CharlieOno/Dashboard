export default {
    install(Vue, options) {
        window.fbAsyncInit = function() {
            FB.init({
                appId      : '992049681147955',
                cookie     : true,
                status     : true,
                xfbml      : true,
                version    : 'v5.0'
            });
            FB.AppEvents.logPageView();
            Vue.FB = FB;
        };
        Vue.FB = undefined;
        (function(d, s, id){
            var js, fjs = d.getElementsByTagName(s)[0];
            if (d.getElementById(id)) {return;}
            js = d.createElement(s); js.id = id;
            js.src = "https://connect.facebook.net/en_US/sdk.js";
            fjs.parentNode.insertBefore(js, fjs);
        }(document, 'script', 'facebook-jssdk'));
    }
}