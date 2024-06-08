# Source: https://github.com/KMKfw/kmk_firmware/issues/409
from kmk.keys import KC, make_key


mods_before_modmorph = set()
def modmorph(names = {'DUMMY_KEY',}, default_kc = KC.NO, morphed_kc = KC.NO, triggers = {KC.LSHIFT, KC.RSHIFT}):
    def _pressed(key, state, KC, *args, **kwargs):
        global mods_before_modmorph
        mods_before_modmorph = triggers.intersection(state.keys_pressed)
        # if a trigger is held, morph key
        if mods_before_modmorph:
            state._send_hid()
            for mod_kc in mods_before_modmorph:
                # discard triggering mods so morphed key is unaffected by them
                state.keys_pressed.discard(mod_kc)
            state.keys_pressed.add(morphed_kc)
            state.hid_pending = True
            return state
        # else return default keycode
        state.keys_pressed.add(default_kc)
        state.hid_pending = True
        return state
    def _released(key, state, KC, *args, **kwargs):
        if {morphed_kc,}.intersection(state.keys_pressed):
            state.keys_pressed.discard(morphed_kc)
            for mod_kc in mods_before_modmorph:
                # re-add previously discarded shift so normal typing isn't impacted
                state.keys_pressed.add(mod_kc)
        else:
            state.keys_pressed.discard(default_kc)
        state.hid_pending = True
        return state
    modmorph_key = make_key(names=names, on_press=_pressed,
                            on_release=_released)
    return modmorph_key
