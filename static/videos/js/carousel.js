// Pausar o vídeo anterior quando um novo vídeo for iniciado
document.querySelectorAll('.video-player').forEach(function (video) {
    video.addEventListener('play', function () {
        document.querySelectorAll('.video-player').forEach(function (otherVideo) {
            if (otherVideo !== video) {
                otherVideo.pause(); // Pausa os outros vídeos
            }
        });
    });
});

