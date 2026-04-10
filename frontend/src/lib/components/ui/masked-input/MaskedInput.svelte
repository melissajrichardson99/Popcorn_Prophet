<script lang="ts">
  import { onMount, tick } from "svelte";

  let {
    value = $bindable(),
    errs = $bindable({}),
    is_dirty = $bindable(),
    required = false,
    ...rest
  } = $props();

  let this_input: HTMLInputElement;

  let aria_invalid = $state<boolean | undefined>(undefined);

  const currency_formatter = new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });

  function is_numeric(key: string) {
    return "0" <= key && key <= "9";
  }

  function is_arrow_key(key: string) {
    return key === "ArrowLeft" || key === "ArrowRight";
  }

  function is_backspace(key: string) {
    return key === "Backspace";
  }

  function is_ctrl_a(key: any) {
    return (
      (key.keyCode === 65 || key.keyCode === 97) && (key.ctrlKey || key.metaKey)
    );
  }

  function convert_back_to_number(str: string): string {
    return str.replaceAll(/\$|\,|\./gi, "");
  }

  function mask_input(e: KeyboardEvent) {
    const target = e.target! as HTMLInputElement;

    if (target.value === "") {
      return;
    }

    if (target.value === "$") {
      target.value = "";
      value = "";
      return;
    }

    const caretPositionBefore = target.selectionStart!;
    let previousNumberOfSymbol = null;

    if (target.value.startsWith("$")) {
      previousNumberOfSymbol = target.value.match(/\$|\,|\./gi)!.length;
      value = convert_back_to_number(target.value);
      this_input.value = currency_formatter.format(parseInt(value))
    } else {
      value = parseInt(target.value);
      this_input.value = currency_formatter.format(value)
    }

    if (is_numeric(e.key) || is_backspace(e.key)) {
      const currNumberOfSymbol = target.value.match(/\$|\,|\./gi)!.length;
      const diff = currNumberOfSymbol - previousNumberOfSymbol!;
      target.setSelectionRange(
        caretPositionBefore + diff,
        caretPositionBefore + diff,
      );
    }

    is_dirty = true;
    // FIXME: bug occurs when users delete the dollar symbol
  }

  function keydown(e: KeyboardEvent) {
    if (
      is_numeric(e.key) ||
      is_arrow_key(e.key) ||
      is_ctrl_a(e) ||
      is_backspace(e.key)
    ) {
      return;
    }
    e.preventDefault();
  }

  $effect(() => {
    if (required) {
      if (!value) {
        if (!errs['required']) {
          errs['required'] = "Value cannot be empty";
        }
      } else {
        if (errs['required'])  {
          delete errs['required'];
        }
      }
    }
  });

  $effect(() => {
    aria_invalid = Object.keys(errs).length > 0 && is_dirty === true;
  });

  $effect(() => {
    if (value) {
      this_input.value = currency_formatter.format(parseInt(value))
    }
  })
</script>

<input
  class="bg-dark-blue-4 text-white h-9 px-3 py-2 rounded-md border border-blue-gray-2 w-full aria-invalid:border-destructive focus:aria-invalid:outline-none"
  onkeyup={mask_input}
  onkeydown={keydown}
  aria-invalid={aria_invalid}
  {required}
  bind:this={this_input}
  {...rest}
/>
