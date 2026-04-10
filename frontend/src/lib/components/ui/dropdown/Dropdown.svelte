<script lang="ts">
  import * as Select from "$lib/components/ui/select/index.js";
  let {
    value = $bindable(null),
    errs = $bindable({}),
    is_dirty = $bindable(false),
    required = false,
    options,
    on_value_change = null,
  } = $props();

  let aria_invalid = $state<boolean | undefined>(undefined);

  $effect(() => {
    aria_invalid = Object.keys(errs).length > 0 && is_dirty;
  })

  $effect(() => {
    if (required) {
      if (!value) {
        if (!errs['required']) {
          errs['required'] = "Value cannot be empty";
        }
      } else {
        if (errs['required']) {
          delete errs['required'];
        }
      }
    }
  })

  function on_change() {
    is_dirty = true;
    if (on_value_change) {
      on_value_change();
    }
  }
</script>

<Select.Root type="single" bind:value onValueChange={on_change} allowDeselect={true}>
  <Select.Trigger class="w-full" aria-required={required} aria-invalid={aria_invalid}>{options[value]}</Select.Trigger>
  <Select.Content>
    {#each Object.entries(options) as [value, label]}
      <Select.Item {value}>{label}</Select.Item>
    {/each}
  </Select.Content>
</Select.Root>
