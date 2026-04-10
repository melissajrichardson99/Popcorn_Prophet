<script lang="ts">
  let {
    value = $bindable(),
    errs = $bindable({}),
    is_dirty = $bindable(),
    min = null,
    max = null,
    required = false,
    suffix = null,
    type = "text",
    ...rest
  } = $props();

  let aria_invalid = $state<boolean | undefined>(undefined);

  $effect(() => {
    aria_invalid = Object.keys(errs).length > 0 && is_dirty === true;
  })

  function is_numeric(key: string) {
    return "0" <= key && key <= "9";
  }

  function is_arrow_key(key: string) {
    return key === 'ArrowLeft' || key === "ArrowRight";
  }

  function is_backspace(key: string) {
    return key === "Backspace";
  }

  function is_ctrl_a(key: any) {
    return (key.keyCode === 65 || key.keyCode === 97) && (key.ctrlKey || key.metaKey);
  }

  function on_key_down(e: KeyboardEvent) {
    if (type === "number") {
      if (!is_numeric(e.key) && !is_backspace(e.key) && !is_arrow_key(e.key) && !is_ctrl_a(e.key)) {
        e.preventDefault();
      }
    }
  }

  $effect(() => {
    if (type === "number") {
      const val = parseInt(value);
      if (max) {
        if (val > max) {
          if (!errs["max"])
            errs["max"] = `Value must be smaller or equal to ${max}`;
        } else {
          if (errs["max"]) delete errs["max"];
        }
      }

      if (min) {
        if (val < min) {
          if (!errs["min"])
            errs["min"] = `Value must be larger or equal to ${min}`;
        } else {
          if (errs["min"]) delete errs["min"];
        }
      }
    }

    if (required !== null && required !== undefined) {
      if (value === null || value === undefined) {
        if (!errs["required"]) errs["required"] = `Value cannot be empty`;
      } else {
        if (errs["required"]) delete errs["required"];
      }
    }
  })

  function on_input(_e: KeyboardEvent) {
    is_dirty = true;
  }
</script>

<!-- TODO: Figure out how to do outline and ring when input is invalid -->
<div class="relative">
  <input
    {type}
    class="relative bg-dark-blue-4 text-white h-9 px-3 py-2 rounded-md border border-blue-gray-2 w-full aria-invalid:border-destructive focus:aria-invalid:outline-none appearance:textfield] [&::-webkit-inner-spin-button]:m-0 [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:m-0 [&::-webkit-outer-spin-button]:appearance-none"
    bind:value
    onkeydown={on_key_down}
    oninput={on_input}
    aria-invalid={aria_invalid}
    max={max}
    min={min}
    required={required}
    {...rest}
  />
  {#if suffix}
    <span class="absolute text-light-gray translate-y-1/4 -translate-x-[130%]">mins</span>
  {/if}
</div>
