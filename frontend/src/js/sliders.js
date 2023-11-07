// core version + navigation, pagination modules:
import Swiper from "swiper";
import { Navigation } from "swiper/modules";
import "../scss/_swiper";

// init Swiper:
const swiper = new Swiper(".swiper", {
	// configure Swiper to use modules
	modules: [Navigation],
});
