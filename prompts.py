def build_instruction(opts: dict, require_json: bool = False) -> str:
    """
    Build a detailed instruction for Gemini based on opts.
    opts: {
      description_type, tone, output_length, detail_level,
      extra_instructions, style_prompt, return_format
    }
    If require_json True, ask model to return strict JSON.
    """

    description_type = opts.get("description_type", "Describe in Detail")
    tone = opts.get("tone", "Friendly")
    output_length = opts.get("output_length", "Large")
    detail_level = opts.get("detail_level", "Deep")
    extra = opts.get("extra_instructions")
    style_prompt = opts.get("style_prompt")
    return_format = opts.get("return_format", "text")

    lines = [
        "You are an expert image describer. Follow instructions exactly.",
        f"Description Type: {description_type}",
        f"Tone: {tone}",
        f"Output Length: {output_length}",
        f"Detail Level: {detail_level}",
        "",
        "Produce the following sections when applicable:",
        "1) title (1 line)",
        "2) long_description (2-4 paragraphs for Large, 1 paragraph for Medium, 2-3 sentences for Small)",
        "3) key_objects (comma-separated list)",
        "4) colors_and_mood (short)",
        "5) alt_text (one concise sentence)",
        "6) seo_summary (2-3 lines)",
        "7) tags_hashtags (10 tags or hashtags)",
        "8) prompt_conversions (if requested: Midjourney, Stable Diffusion, Flux) -- provide one-line prompts",
        ""
    ]

    # Give explicit length guidance
    if output_length.lower() == "small":
        lines.append("Keep the long_description to 2-3 short sentences.")
    elif output_length.lower() == "medium":
        lines.append("Keep the long_description to one well-structured paragraph (4-6 sentences).")
    else:
        lines.append("Make the long_description rich and descriptive: sensory details, context, composition, likely materials, and plausible backstory. Use 2-4 paragraphs.")

    # Detail level
    if detail_level.lower() == "simple":
        lines.append("Avoid technical jargon; use plain language and short sentences.")
    else:
        lines.append("Include deeper analysis (composition, artistic references, likely camera/lens if photo, materials if object, cultural/historical references when relevant).")

    if extra:
        lines.append(f"Extra instructions: {extra}")

    if style_prompt:
        lines.append(f"Also convert description into style prompt: {style_prompt} (append in Prompt Conversions).")

    # Output formatting
    if require_json or return_format == "json":
        lines.append("")
        lines.append("IMPORTANT: Return a single valid JSON object with these keys:")
        lines.append('{"title","description","objects","colors_mood","alt_text","seo","tags","prompt_conversions"}')
        lines.append("If a field is not applicable, return an empty string or empty array. Do not add extra commentary outside the JSON.")
    else:
        lines.append("")
        lines.append("Return clean plain text with the sections labeled as above. No extra commentary.")

    return "\n".join(lines)
