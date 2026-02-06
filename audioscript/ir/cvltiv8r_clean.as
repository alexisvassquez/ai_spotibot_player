track "cvltiv8r_clean" {

    bpm 128

    section "intro" from 0.000 to 8.000 {
        at 0.000 {
            leds.ambient(front_strip, intensity: 0.30);
        }
    }

    section "build" from 8.000 to 24.000 {
        at 8.000 {
            leds.rise_all(duration: 16.00);
        }
    }

    section "drop" from 24.000 to 48.000 {
        at 24.000 {
            leds.flash_all(strobe_intensity: 1.00);
        }
    }

    section "outro" from 48.000 to 60.000 {
        at 48.000 {
            leds.fade_all(duration: 12.00);
        }
    }

}
