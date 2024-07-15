import { AspectRatio, Box } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

// get logged in username function
const useMiscFunctions = () => {

    const cloudName = process.env.REACT_APP_CLOUDINARY_NAME || 'your cloudinary name';
    const uploadPreset = process.env.REACT_APP_CLOUDINARY_PRESET || 'your cloudinary preset';
    const api_key = process.env.REACT_APP_CLOUDINARY_API || 'your cloudinary api';

    // handle logout
    const navigate = useNavigate();

    const handleLogout = () => {

        localStorage.removeItem("access_token");
        navigate('/login');

    };

    const LazyLoadYoutubeEmbed = ({ youtubeLink }: { youtubeLink: string }) => {

        const roundframe = {
            borderRadius: "15px",
            overflow: "hidden",
        };
        const youtubeID = youtubeLink.split("v=")[1]
        return (
            <Box mt={1}  >

                <AspectRatio ratio={16 / 9}>
                    <iframe
                        title={`Youtube VideoID: ${youtubeID}`}
                        style={roundframe}
                        src={`https://www.youtube.com/embed/${youtubeID}`
                        }
                        srcDoc={`<style>
                            *{padding:0;margin:0;overflow:hidden}html,body{height:100%}img,
                            span{position:absolute;width:100%;top:0;bottom:0;margin:auto}
                            span{height:1.5em;text-align:center;font:48px/1.5 sans-serif;color:white;text-shadow:0 0 0.5em black}
                            </style>
                            <a href=https://www.youtube.com/embed/${youtubeID}?autoplay=1>
                            <img src=https://img.youtube.com/vi/${youtubeID}/hqdefault.jpg><span>▶</span></a>"`}
                        allowFullScreen
                    />
                </AspectRatio>

            </Box>
        );
    };


    return { cloudName, uploadPreset, api_key, handleLogout, LazyLoadYoutubeEmbed }


};

export default useMiscFunctions;