import React, { useEffect, useRef } from 'react';
import './App.css';

// Dynamically import all video files from the src folder
const requireContext = require.context('./sample_video/', false, /\.(mp4)$/);
const videoSources = requireContext.keys().map(requireContext);

console.log(videoSources); // Log the video sources for debugging

function App() {
  const videoRefs = useRef([]);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach(entry => {
          const video = entry.target;
          if (entry.isIntersecting) {
            video.play().catch(error => {
              console.log("Auto-play was prevented: ", error);
            });
          } else {
            video.pause();
          }
        });
      },
      {
        threshold: 0.5, // Adjust this threshold as needed
      }
    );

    const currentVideoRefs = videoRefs.current;
    currentVideoRefs.forEach(video => {
      if (video) {
        observer.observe(video);
      }
    });

    return () => {
      currentVideoRefs.forEach(video => {
        if (video) {
          observer.unobserve(video);
        }
      });
    };
  }, []);

  return (
    <div className="App">
      <div className="banner">Hentaireel</div>
      <div className="search-bar">
        <input type="text" placeholder="Search..." />
      </div>
      <div className="video-count">
        Loaded {videoSources.length} videos
      </div>
      <div className="video-container">
        {videoSources.map((videoSrc, index) => {
          console.log(`Rendering video ${index}: ${videoSrc}`); // Log each video rendering
          return (
            <div className="App-header" key={index}>
              <video
                className="App-video"
                controls
                muted
                ref={el => (videoRefs.current[index] = el)}
              >
                <source src={videoSrc} type="video/mp4" />
                Your browser does not support the video tag.
              </video>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default App;
