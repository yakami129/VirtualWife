// import { useEffect, useState } from 'react';

// export const PhotoFrame = ({ imageUrl }) => {

//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(false);

//   useEffect(() => {
//     fetch(imageUrl)
//       .then((response) => {
//         if (!response.ok) {
//           throw new Error('Network response was not ok');
//         }
//         setLoading(false);
//       })
//       .catch(() => setError(true));
//   }, [imageUrl]);

//   if (loading) {
//     return <div className="photo-frame">Loading...</div>;
//   }

//   if (error) {
//     return <div className="photo-frame">Error loading image</div>;
//   }

//   return (
//     <div className="photo-frame">
//       <img src={imageUrl} alt="User provided" />
//     </div>
//   );
// };