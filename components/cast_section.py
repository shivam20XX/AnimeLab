import streamlit as st


def render_cast_sections(anime):
    characters = anime.get("characters", {}).get("edges", [])

    if characters:
        st.markdown("## Characters")
        columns = st.columns(min(8, len(characters)))

        for index, edge in enumerate(characters[:8]):
            character = edge.get("node", {})

            with columns[index]:
                image = character.get("image", {}).get("large")

                if image:
                    st.image(image, use_container_width=True)

                name = (
                    character.get("name", {}).get("full")
                    or "Unknown"
                )

                st.markdown(f"**{name}**")
                st.caption(edge.get("role") or "Unknown")

    # Voice Cast
    cast_items = []
    seen_actor_ids = set()

    for edge in characters:
        for voice_actor in edge.get("voiceActors") or []:
            actor_id = voice_actor.get("id")

            if actor_id is not None and actor_id in seen_actor_ids:
                continue

            if actor_id is not None:
                seen_actor_ids.add(actor_id)

            cast_items.append({
                "image": voice_actor.get("image", {}).get("large"),
                "actor_name": (
                    voice_actor.get("name", {}).get("full")
                    or "Unknown"
                ),
                "character_name": (
                    edge.get("node", {})
                    .get("name", {})
                    .get("full")
                    or "Unknown"
                ),
            })

            if len(cast_items) >= 8:
                break

        if len(cast_items) >= 8:
            break

    if cast_items:
        st.markdown("## Voice Cast")
        columns = st.columns(len(cast_items))

        for index, cast in enumerate(cast_items):
            with columns[index]:
                if cast["image"]:
                    st.image(
                        cast["image"],
                        use_container_width=True,
                    )

                st.markdown(f"**{cast['actor_name']}**")
                st.caption(f"as {cast['character_name']}")

    # Staff
    staff = anime.get("staff", {}).get("edges", [])

    if staff:
        st.markdown("## Staff & Crew")
        staff_items = staff[:8]
        columns = st.columns(len(staff_items))

        for index, edge in enumerate(staff_items):
            person = edge.get("node", {})

            with columns[index]:
                image = person.get("image", {}).get("large")

                if image:
                    st.image(image, use_container_width=True)

                name = (
                    person.get("name", {}).get("full")
                    or "Unknown"
                )

                st.markdown(f"**{name}**")
                st.caption(edge.get("role") or "Unknown")