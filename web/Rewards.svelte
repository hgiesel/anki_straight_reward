<script>
    const {
        TitledContainer,
        SpinBoxRow,
        SpinBoxFloatRow,
        SwitchRow,
    } = anki.components;

    export let data;
</script>

<TitledContainer title="Rewards">
    <SpinBoxRow
        bind:value={$data.straightLength}
        defaultValue={1}
        markdownTooltip=""
    >
        Begin at straight of length
    </SpinBoxRow>

    <SpinBoxFloatRow
        bind:value={$data.baseEase}
        defaultValue={0.05}
        markdownTooltip=""
    >
        Base ease reward
    </SpinBoxFloatRow>

    <SpinBoxFloatRow
        bind:value={$data.stepEase}
        defaultValue={0.05}
        markdownTooltip=""
    >
        Step ease reward
    </SpinBoxFloatRow>

    <SpinBoxFloatRow
        bind:value={$data.startEase}
        defaultValue={1.30}
        markdownTooltip=""
    >
        Start at ease
    </SpinBoxFloatRow>

    <SpinBoxFloatRow
        bind:value={$data.stopEase}
        defaultValue={2.50}
        markdownTooltip=""
    >
        Stop at ease
    </SpinBoxFloatRow>

    <SwitchRow
        bind:value={$data.enableNotification}
        defaultValue={true}
        markdownTooltip=""
    >
        Enable notification
    </SwitchRow>
</TitledContainer>
