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

  let selectionText = $derived(value.map((v: any) => options[v]).join(", "));
  let aria_invalid = $state<boolean | undefined>(undefined);

  $effect(() => {
    if (required) {
      if (!value.length) {
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

  $effect(() => {
    aria_invalid = is_dirty && Object.keys(errs).length > 0;
  })

  function on_change() {
    is_dirty = true;
    if (on_value_change) {
      on_value_change();
    }
  }
</script>

<Select.Root type="multiple" bind:value onValueChange={on_change}>
  <Select.Trigger class="w-full" aria-required={required} aria-invalid={aria_invalid}>
    <div class="overflow-hidden text-ellipsis">{selectionText}</div>
  </Select.Trigger>
  <Select.Content>
    {#each Object.entries(options) as [value, label]}
      <Select.Item {value}>{label}</Select.Item>
    {/each}
  </Select.Content>
</Select.Root>
